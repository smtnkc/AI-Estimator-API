import json
import argparse


def create_predict_result(job_id, job_priority, user_id, project_name, in_model_name, target_metric):
    with open('temp_results.json', 'r') as f:
        data = json.load(f)

    # Process and create the final JSON structure
    predict_result = {
        "job_id": job_id,
        "job_priority": job_priority,
        "user_id": user_id,
        "project_name": project_name,
        "in_model_name": in_model_name,
        "target_metric": target_metric,
        "predictions": data["predictions"]
    }

    # Write to predict_result.json
    with open('JSON/predict_result.json', 'w') as f:
        json.dump(predict_result, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--job_priority", required=True)
    parser.add_argument("--user_id", required=True)
    parser.add_argument("--project_name", required=True)
    parser.add_argument("--in_model_name", required=True)
    parser.add_argument("--target_metric", required=True)

    args = parser.parse_args()

    create_predict_result(args.job_id, args.job_priority, args.user_id, args.project_name, args.in_model_name,
                          args.target_metric)
