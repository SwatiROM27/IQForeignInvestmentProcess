import csv
import re
from ranking import read_csv, get_company_analysis


def parse_markdown_row(markdown_row):
    parts = markdown_row.strip().strip("|").split("|")
    return [part.strip() for part in parts]


def main():
    input_file = "Project/IQTest.csv"
    output_file = "Project/output.csv"

    input_data = read_csv(input_file)

    if not input_data:
        print("No data found.")
        return

    original_headers = list(input_data[0].keys())

    gpt_fields = [
        "GPT Score",
        "GPT Score Explanation",
        "GPT Dutch Ecosystem Fit & Chain Partners",
        "GPT Sources Details"
    ]

    reordered_headers = (
        ["Nr", "Firm name"]
        + gpt_fields
        + [field for field in original_headers if field not in ["Nr", "Firm name"]]
    )

    with open(output_file, "w", newline='', encoding="utf-8") as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=reordered_headers)
        writer.writeheader()

        for idx, row in enumerate(input_data, 1):
            print(f"Processing row {idx}: {row.get('Firm name')}")
            markdown_row = get_company_analysis(row)
            print(f"AI Response for row {idx}: {markdown_row[:200]}...")

            try:
                lines = markdown_row.split('\n')
                score = "N/A"
                explanation = ""
                ecosystem_fit = ""
                sources_details = ""

                for line in lines:
                    if line.strip().startswith('|') and '|' in line and len(line.split('|')) >= 5:
                        parsed = parse_markdown_row(line)
                        if len(parsed) >= 5:
                            _, score, explanation, ecosystem_fit, sources_details = parsed[:5]
                            break

                if score == "N/A":
                    score_patterns = [
                        r'score[:\s]*(\d{1,3})',
                        r'rating[:\s]*(\d{1,3})',
                        r'(\d{1,3})/100',
                        r'(\d{1,3})\s*out\s*of\s*100',
                        r'assessment[:\s]*(\d{1,3})'
                    ]
                    for line in lines:
                        for pattern in score_patterns:
                            match = re.search(pattern, line.lower())
                            if match:
                                score_val = int(match.group(1))
                                if 0 <= score_val <= 100:
                                    score = str(score_val)
                                    break
                        if score != "N/A":
                            break

                    meaningful_lines = []
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('|') and not line.startswith('ANALYSIS:') and len(line) > 20:
                            meaningful_lines.append(line)
                            if len(meaningful_lines) >= 3:
                                break
                    if meaningful_lines:
                        explanation = ' '.join(meaningful_lines)
                        words = explanation.split()
                        if len(words) > 100:
                            explanation = ' '.join(words[:100]) + "..."

                    dutch_mentions = [
                        line.strip() for line in lines
                        if any(word in line.lower() for word in ['dutch', 'netherlands', 'amsterdam', 'rotterdam', 'eindhoven'])
                    ]
                    if dutch_mentions:
                        ecosystem_fit = ' '.join(dutch_mentions[:2])
                        words = ecosystem_fit.split()
                        if len(words) > 100:
                            ecosystem_fit = ' '.join(words[:100]) + "..."
                    else:
                        ecosystem_fit = "No specific Dutch market mention found"

                    # Extract sources details from text if not found in table
                    if not sources_details:
                        sources_mentions = []
                        for line in lines:
                            if any(word in line.lower() for word in ['linkedin', 'website', 'news', 'source', 'patent', 'trade', 'industry', 'regulatory', 'publication', 'database', 'project', 'accelerator', 'portxl', 'buccaneer', 'horizon', 'interreg', 'emsa', 'imo']):
                                sources_mentions.append(line.strip())
                        
                        if sources_mentions:
                            sources_details = ' '.join(sources_mentions[:4])  # Take up to 4 sources
                            if len(sources_details) > 250:
                                sources_details = sources_details[:250] + "..."
                        else:
                            sources_details = "No specific sources mentioned"

                enriched_row = {
                    **row,
                    gpt_fields[0]: score,
                    gpt_fields[1]: explanation,
                    gpt_fields[2]: ecosystem_fit,
                    gpt_fields[3]: sources_details
                }

                ordered_row = {field: enriched_row.get(field, "") for field in reordered_headers}
                writer.writerow(ordered_row)

            except Exception as e:
                print(f"❌ Failed to process row {idx}: {e}")
                continue


if __name__ == "__main__":
    main()
