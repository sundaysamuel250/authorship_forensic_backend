# api/views.py
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import tempfile

class AnalyzeTextView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file", None)
        text = request.POST.get("text", "")

        # Extract text from uploaded file
        if file:
            ext = os.path.splitext(file.name)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
                for chunk in file.chunks():
                    temp.write(chunk)
                temp_path = temp.name

            try:
                if ext == ".txt":
                    with open(temp_path, "r", encoding="utf-8") as f:
                        text = f.read()
                elif ext == ".pdf":
                    import PyPDF2
                    reader = PyPDF2.PdfReader(temp_path)
                    text = "\n".join([page.extract_text() for page in reader.pages])
                else:
                    return Response({"error": "Unsupported file format."}, status=400)
            finally:
                os.unlink(temp_path)

        if not text:
            return Response({"error": "No text provided."}, status=400)

        # Dummy prediction (replace with your ML logic)
        import random
        prediction = random.choice(["AI", "Human"])
        confidence = round(random.uniform(80, 99), 2)

        result = {
            "author": prediction,
            "confidence": confidence,
            "stylometry": {
                "featureNames": ["avg_word_length", "vocab_richness"],
                "values": [4.7, 0.82],
            },
            "heatmap": {
                "matrix": [[1, 0.75], [0.75, 1]],
                "labels": ["Feature A", "Feature B"],
            }
        }

        return Response(result, status=status.HTTP_200_OK)
