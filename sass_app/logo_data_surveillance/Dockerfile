FROM brand_dataset_manager:0.1
WORKDIR /home/admin/playground
ADD app.py .
EXPOSE 8088
CMD ["gunicorn", "-b", "0.0.0.0:8088", "-w", "1", "app:app", "-t", "30000"]
