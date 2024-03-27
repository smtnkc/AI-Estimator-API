import sys
import json
import csv
import os
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--user_id")
    parser.add_argument("--project_name")
    parser.add_argument("--in_model")
    parser.add_argument("--in_column")
    parser.add_argument("--out_column")
    parser.add_argument("--out_model")
    args=parser.parse_args()

    base_path= f"{args.user_id}"
    dataset_path=os.path.join(base_path,"data",f"data_{args.project_name}.csv")
    preds_path=os.path.join(base_path,"preds",f"{args.out_model}.csv")
    scores_path=os.path.join(base_path,"scores",f"{args.out_model}.csv")
    in_model_dir=os.path.join(base_path,"models",f"{args.in_model}/")
    out_model_dir=os.path.join(base_path,"models",f"{args.out_model}/")

    print("dataset_path=",dataset_path)
    print("preds_path=",preds_path)
    print("scores_path=",scores_path)
    print("in_model_dir=",in_model_dir)
    print("out_model_dir=",out_model_dir)
    print("----------------------------")





#doğrudan çalıştırmak için bunu kullandım.
if __name__ == "__main__":
    main()



