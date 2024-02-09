import pandas as pd
import sys
def main():
    def topsis(csv_file, weights, impacts, output_file):
        # Read the CSV file into a DataFrame with the first row as column names
        data = pd.read_csv(csv_file, index_col=0, header=0)

        # Check if the number of weights, impacts, and columns match
        if len(weights) != len(data.columns) or len(impacts) != len(data.columns):
            print("Error: Number of weights and impacts should match the number of columns in the CSV file.")
            return

        # Multiply impacts with weights directly
        weighted_impacts = [w * i for w, i in zip(weights, impacts)]

        # Normalize the data
        norm_data = data.copy()
        for column in data.columns:
            norm_data[column] = data[column] / ((data[column]**2).sum())**0.5

        # Multiply the normalized data by weighted impacts
        for i, col in enumerate(data.columns):
            norm_data[col] *= weighted_impacts[i]

        # Calculate the ideal and negative-ideal solutions
        ideal_best = norm_data.max(axis=0)
        ideal_worst = norm_data.min(axis=0)

        # Calculate the separation measures
        separation_best = ((norm_data - ideal_best)**2).sum(axis=1)**0.5
        separation_worst = ((norm_data - ideal_worst)**2).sum(axis=1)**0.5

        # Calculate the TOPSIS score
        topsis_score = separation_worst / (separation_worst + separation_best)

        # Add the TOPSIS score as a new column
        data['TOPSIS_Score'] = topsis_score

        # Rank the data based on the TOPSIS score
        data['Rank'] = data['TOPSIS_Score'].rank(ascending=False)

        # Save the results to the output file
        data.to_csv(output_file)

        # Display the results
        print(f"Results saved to {output_file}")

    if __name__ == "__main__":
        if len(sys.argv) != 5:
            print("Usage: python topsis.py <csv_file> <weights> <impacts> <output_file>")
        else:
            csv_file = sys.argv[1]
            weights = [float(w) for w in sys.argv[2].split(',')]
            impacts = [1 if i == '+' else -1 for i in sys.argv[3].split(',')]
            output_file = sys.argv[4]

            topsis(csv_file, weights, impacts, output_file)
