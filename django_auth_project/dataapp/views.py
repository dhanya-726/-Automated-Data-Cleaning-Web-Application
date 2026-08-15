
import pandas as pd
import os
from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import FileUploadForm
from .models import UploadedFile


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            # Read file
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            # -------- Analysis --------
            report = {
                "missing": df.isnull().sum().to_dict(),
                "duplicates": int(df.duplicated().sum()),
                "dtypes": df.dtypes.astype(str).to_dict()
            }

            # -------- Cleaning --------

            # 1. Remove exact duplicate rows (allowed)
            df = df.drop_duplicates()
            # 2. Column-wise cleaning (generic)
            for col in df.columns:

                # Convert empty strings to NULL
                df[col] = df[col].replace("", pd.NA)

                # If column is numeric-like
                if pd.api.types.is_numeric_dtype(df[col]):

                    # Convert safely to numeric
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                    # Allowed operations:
                    # Option A: keep NULL  (do nothing)
                    # Option B: fill with 0
                    df[col] = df[col].fillna(0)

                    # Option C (optional):
                    # df[col] = df[col].fillna(df[col].mean())
                    # df[col] = df[col].fillna(df[col].median())

                else:
                    # Non-numeric columns (text, categories, mixed)
                    # Mark missing (allowed)
                    df[col] = df[col].fillna("Missing")

            # 3. Business rule example (optional):
            # Remove rows that are fully empty
            df = df.dropna(how='all')


            # Save cleaned file
            os.makedirs(settings.MEDIA_ROOT / 'cleaned', exist_ok=True)
            cleaned_name = f"cleaned_{file.name.replace(' ', '_')}"
            cleaned_path = settings.MEDIA_ROOT / 'cleaned' / cleaned_name
            df.to_csv(cleaned_path, index=False)

            uploaded = UploadedFile.objects.create(
                user=request.user,
                original_file=file,
                cleaned_file=f"cleaned/{cleaned_name}"
            )

            return render(request, 'dataapp/report.html', {
                'report': report,
                'file_id': uploaded.id
            })
    else:
        form = FileUploadForm()

    return render(request, 'dataapp/upload.html', {'form': form})


@login_required
def download_cleaned(request, file_id):
    obj = UploadedFile.objects.get(id=file_id, user=request.user)
    return FileResponse(open(obj.cleaned_file.path, 'rb'), as_attachment=True)
