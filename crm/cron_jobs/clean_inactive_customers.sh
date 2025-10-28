#!/bin/bash
# Script to delete inactive customers (no orders in the last year)


timestamp=$(date "+%Y-%m-%d %H:%M:%S")
deleted_count=$(python manage.py shell -c "
from crm.models import Customer
from datetime import datetime, timedelta
threshold = datetime.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(order__isnull=True, created_at__lt=threshold).delete()
print(deleted)
")

