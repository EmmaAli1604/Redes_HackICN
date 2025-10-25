## Script: calculate_distfacts.py

Calculates the distfacts for a power grid model.

Required Input Tables (CSV format): 
	branches_<model_name>.csv
		l (Integer): Unique identifier for the branch.
		branch_name (String): The human-readable name of the branch.
		from_bus (Integer): The bus number where the branch originates.
		to_bus (Integer): The bus number where the branch terminates.
		available (Integer): A flag indicating if the branch is in service (1) or out of service (0).

	generators_<model_name>.csv
		gen (String/Integer): A unique identifier for the generator.
		generator_name (String): The unique name of the generator.
		n (Integer): The bus number where the generator is connected.

	loads_<model_name>.csv
		load_name (String): The unique name of the load.
		n (Integer): The bus number where the load is connected.

Output Table: distfacts_<model_name>.csv
	equipment_name (String): Name of the generator or load.
	equipment_type (Integer): Type identifier (e.g., 0 for generator, 1 for load).
	branch_name (String): Name of the transmission line.
	distfact (Float): The calculated shiftfactor.

## Script: calculate_metrics.py

Compares the distfacts from a full and a reduced model.

Required Input Tables (CSV format): 
	distfacts_<full_model_name>.csv (output from the previous script for the full model) 
	distfacts_<reduced_model_name>.csv (output from the previous script for the reduced model) 
	monitored_lines_<model_name>.csv with column
		branch_name (String): A list of the branch names to be included in the analysis.
    
Output Table: distfact_metrics.csv
	reduction_factor (Float): The percentage of branches removed from the full model.
	mse (Float): Mean Squared Error between the full and reduced distfacts.
	rmse (Float): Root Mean Squared Error.
	mae (Float): Mean Absolute Error.
	
	
## How to Run the Example

The goal is to generate a distfacts file for a "full" model and a "reduced" model, and then compare them.

Step 1: Calculate distfacts for the full model with calculate_distfacts. Set the output file name to "distfacts_full.csv". Then run the script: calculate_distfacts.bin
```bash
./calculate_distfacts.bin --branches ./datasets/example/branches_2025-01-15.csv --generators ./datasets/example/generators_2025-01-15.csv --loads ./datasets/example/loads_2025-01-15.csv --out ./distfacts_full.csv
```

Step 2: Calculate distfacts for the reduced model. Set the output file name to "distfacts_reduced.csv". Run the script again: calculate_distfacts.bin
```bash
./calculate_distfacts.bin --branches ./datasets/example/branches_reduced_2025-01-15.csv --generators ./datasets/example/generators_reduced_2025-01-15.csv --loads ./datasets/example/loads_reduced_2025-01-15.csv --out ./distfacts_reduced.csv
```

Step 3: Calculate the comparison metrics. Ensure distfacts_full.csv, distfacts_reduced.csv, and monitored_lines.csv are present. Run the metrics script: calculate_metrics.bin

This will create the final comparison file, distfact_metrics.csv.

```bash
./compare_distfacts.bin --all-distfacts ./distfacts_full.csv --distfacts ./distfacts_reduced.csv --monitored-lines ./datasets/example/monitored_lines_2025-01-15.csv --out ./distfact_metrics.csv
```
