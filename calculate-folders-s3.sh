while IFS= read -r folder; do aws s3 ls s3://bucket/${folder01}/$folder/ --recursive --human-readable --summarize | grep 'Total Size'; done < clients >> total-count