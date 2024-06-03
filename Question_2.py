import pysam
import csv
import pandas as pd

def extract_genotype_info(vcf_file_path, output_csv_path, output_html_path):
    """
    Function that extract genotype information from a vcf file
    """
    # Open the VCF file
    try:
        # Open the VCF file
        vcf = pysam.VariantFile(vcf_file_path)
    except FileNotFoundError:
        print(f"Error: The file {vcf_file_path} was not found.")
        return
    except Exception as e:
        print(f"Error opening the VCF file: {e}")
        return
    
    # Extract sample IDs
    sample_ids = list(vcf.header.samples)
    
    # Open the CSV file for writing
    with open(output_csv_path, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile, delimiter=',')
        
        # Write the header row
        header_row = ["CHROM", "POS", "REF", "ALT"] + sample_ids
        writer.writerow(header_row)
        
        # Process each record in the VCF file
        for record in vcf:
            # Get chromosome, position, reference allele, and alternative allele
            chrom = record.chrom
            pos = record.pos
            ref = record.ref
            alt = record.alts[0] if record.alts else '.'
            
            # Extract genotype information for each sample
            genotypes = ['/'.join(map(str, call['GT'])) for call in record.samples.values()]
            
            # Write the row to the CSV file
            row = [chrom, pos, ref, alt] + genotypes
            writer.writerow(row)
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(output_csv_path)
    print("genotype info:")
    print(df)
    # Save the DataFrame to an HTML file
    df.to_html(output_html_path, index=False)

def extract_allelic_depth_info(vcf_file_path, output_csv_path, output_html_path):
    """
    function that extract allelic depth information from vcf file
    """
    # Open the VCF file
    try:
        # Open the VCF file
        vcf = pysam.VariantFile(vcf_file_path)
    except FileNotFoundError:
        print(f"Error: The file {vcf_file_path} was not found.")
        return
    except Exception as e:
        print(f"Error opening the VCF file: {e}")
        return
    
    # Extract sample IDs
    sample_ids = list(vcf.header.samples)
    
    # Open the CSV file for writing
    with open(output_csv_path, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile, delimiter=',')
        
        # Write the header row
        header_row = ["CHROM", "POS", "REF", "ALT"] + sample_ids
        writer.writerow(header_row)
        
        # Process each record in the VCF file
        for record in vcf:
            # Get chromosome, position, reference allele, and alternative allele
            chrom = record.chrom
            pos = record.pos
            ref = record.ref
            alt = record.alts[0] if record.alts else '.'
            
            # Extract allelic depth information for each sample
            allelic_depths = [','.join(map(str, call['AD'])) for call in record.samples.values()]
            
            # Write the row to the CSV file
            row = [chrom, pos, ref, alt] + allelic_depths
            writer.writerow(row)
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(output_csv_path)
    print("allelic depth info:")
    print(df)
    # Save the DataFrame to an HTML file
    df.to_html(output_html_path, index=False)
    

def phase_genotypes(vcf_file_path, output_csv_path, output_html_path):
    """
    function that extract genotype info based on the depth allelic value
    """
    try:
        # Open the VCF file
        vcf = pysam.VariantFile(vcf_file_path)
    except FileNotFoundError:
        print(f"Error: The file {vcf_file_path} was not found.")
        return
    except Exception as e:
        print(f"Error opening the VCF file: {e}")
        return
    
    # Initialize lists to store the output
    chroms, positions, refs, alts = [], [], [], []
    phased_genotypes = []

    # Get the sample IDs
    sample_ids = vcf.header.samples
    
    # Process each record in the VCF file
    for record in vcf:
        chroms.append(record.chrom)
        positions.append(record.pos)
        refs.append(record.ref)
        alts.append(record.alts[0])
        
        sample_phases = []
        for sample in sample_ids:
            genotype = record.samples[sample]['GT']
            allelic_depth = record.samples[sample].get('AD')
            
            if genotype in [(0, 1), (1, 0)] and allelic_depth:
                allele_1_depth = allelic_depth[0]
                allele_2_depth = allelic_depth[1]
                
                # Determine the allele with the highest depth
                if allele_1_depth >= allele_2_depth:
                    phased_genotype = '0'
                else:
                    phased_genotype = '1'
            else:
                if genotype == (0, 0):
                    phased_genotype = '0'
                elif genotype == (1, 1):
                    phased_genotype = '1'
                else:
                    phased_genotype = '.'
            
            sample_phases.append(phased_genotype)
        
        phased_genotypes.append(sample_phases)
    
    # Create a DataFrame for the output
    data = {
        'CHROM': chroms,
        'POS': positions,
        'REF': refs,
        'ALT': alts
    }
    phased_genotypes_df = pd.DataFrame(phased_genotypes, columns=sample_ids)
    
    output_df = pd.concat([pd.DataFrame(data), phased_genotypes_df], axis=1)
    print("Phased genotype formated:")
    print(output_df)
    # Save to a CSV file
    output_df.to_csv(output_csv_path, index=False)
    
    # Save to an HTML file with good presentation
    output_df.to_html(output_html_path, index=False, justify='center')
    
if __name__ == '__main__':
    # Paths to the input VCF file and output files
    vcf_file_path = 'Pf_M76611.pf7.200_samples.vcf'
    genotype_csv_path = 'genotype_info.csv'
    genotype_html_path = 'genotype_info.html'
    allelic_depth_csv_path = 'allelic_depth_info.csv'
    allelic_depth_html_path = 'allelic_depth_info.html'
    phased_genotypes_csv_path = 'phased_genotypes.csv'
    phased_genotypes_html_path = 'phased_genotypes.html'

    # Extract and save genotype information
    extract_genotype_info(vcf_file_path, genotype_csv_path, genotype_html_path)

    # Extract and save allelic depth information
    extract_allelic_depth_info(vcf_file_path, allelic_depth_csv_path, allelic_depth_html_path)

    # Optional
    phase_genotypes(vcf_file_path, phased_genotypes_csv_path, phased_genotypes_html_path)

    print(f"""Output written to CSV and HTML files:
        for question1 in {genotype_csv_path} and {genotype_html_path},
        for question2 in {allelic_depth_csv_path} and {allelic_depth_html_path}
        and for question3 in {phased_genotypes_csv_path} and {phased_genotypes_html_path}""")
