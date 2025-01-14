from collections import defaultdict
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UploadedFileSerializer
from .models import UploadedFile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO  # Pour gérer les flux de données en mémoire
import base64  # Pour encoder les images en format Base64
from django.http import JsonResponse  # Pour renvoyer des réponses JSON

import math


class UploadedFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fichiers téléchargés.
    Fournit des méthodes pour les opérations CRUD et des actions supplémentaires
    pour prévisualiser les fichiers et accéder à des lignes/colonnes spécifiques.
    """
    serializer_class = UploadedFileSerializer
    queryset = UploadedFile.objects.all()

    def get_object(self):
        """
        Récupère l'objet en utilisant l'ID (pk) fourni dans l'URL.
        """
        try:
            uploaded_file = get_object_or_404(UploadedFile, pk=self.kwargs['pk'])
            print(f"Fichier récupéré : {uploaded_file.id}, Chemin : {uploaded_file.file.path}")
            return uploaded_file
        except KeyError:
            raise Exception("L'ID du fichier est manquant dans la requête.")

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """
        Action pour prévisualiser les premières lignes du fichier CSV.
        """
        try:
            # Récupérer le fichier à partir de l'ID
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path

            # Lire les 7 premières lignes avec pandas
            df = pd.read_csv(file_path)

            # Nettoyer les valeurs NaN et infinies
            def safe_value(value):
                if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                    return None  # Remplace NaN ou infini par None
                return value

            # Convertir les données pour l'aperçu en JSON compatible
            preview_data = df.head(7).applymap(safe_value).to_dict(orient='records')

            # Retourner la prévisualisation
            return Response({"preview": preview_data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['get'], url_path='get_row/(?P<row_index>[0-9]+)')
    def get_row(self, request, pk=None, row_index=None):
        """
        Action pour récupérer une ligne spécifique par son index.
        """
        try:
            # Récupérer le fichier à partir de l'ID
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path

            # Lire le fichier avec pandas
            df = pd.read_csv(file_path)

            # Convertir row_index en entier
            row_index = int(row_index)

            # Vérifier si l'index est valide
            if row_index < 0 or row_index >= len(df):
                return Response({"error": "Index de ligne invalide."}, status=400)

            # Récupérer la ligne
            row_data = df.iloc[row_index].to_dict()

            # Retourner la ligne demandée
            return Response({"row_data": row_data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['get'], url_path='get_column/(?P<column_name>.+)')
    def get_column(self, request, pk=None, column_name=None):
        """
        Action pour récupérer une colonne spécifique par son nom.
        """
        try:
            # Récupérer le fichier à partir de l'ID
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path

            # Lire le fichier avec pandas
            df = pd.read_csv(file_path)

            if column_name not in df.columns:
                return Response({
                    "error": f"Colonne '{column_name}' non trouvée.",
                    "available_columns": list(df.columns)
                }, status=400)

            # Récupérer la colonne
            column_data = df[column_name].tolist()

            # Retourner la colonne demandée
            return Response({"column_data": column_data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['get'], url_path='analyze_columns')
    def analyze_columns(self, request, pk=None):
        """
        Action pour analyser toutes les colonnes du fichier CSV et calculer des statistiques.
        """
        try:
         # Récupérer le fichier à partir de l'ID
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path

        # Lire le fichier avec pandas
            df = pd.read_csv(file_path)

        # Initialiser le dictionnaire des statistiques
            analysis = {}

        # Analyser chaque colonne
            for column in df.columns:
                column_data = df[column].dropna()  # Supprimer les valeurs manquantes

            # Calcul des statistiques pour les données numériques
                if pd.api.types.is_numeric_dtype(column_data):
                    stats = {
                        'mean': column_data.mean(),
                        'median': column_data.median(),
                        'min': column_data.min(),
                        'max': column_data.max(),
                        'stddev': column_data.std()
                    }
                    analysis[column] = {
                        'type': 'numeric',
                        'mean': stats['mean'],
                        'median': stats['median'],
                        'min': stats['min'],
                        'max': stats['max'],
                        'stddev': stats['stddev']
                    }
                else:
                # Si ce n'est pas une colonne numérique, on affiche des statistiques de base
                    analysis[column] = {
                        'type': 'non-numeric',
                        'uniqueValues': column_data.unique().tolist(),
                        'count': column_data.count()
                    }

        # Retourner les résultats de l'analyse
            return Response({"analysis": analysis}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
    @action(detail=True, methods=['get'], url_path='plot')
    def generate_plot(self, request, pk=None):
        """
        Action pour générer un graphique à partir de la colonne sélectionnée.
    """
        try:
        # Récupérer le fichier à partir de l'ID
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path

        # Lire le fichier avec pandas
            df = pd.read_csv(file_path)

            column_name = request.query_params.get('x')
            chart_type = request.query_params.get('chart_type')

            if column_name not in df.columns:
                return Response({"error": f"Colonne '{column_name}' non trouvée."}, status=400)

        # Créer un graphique en fonction du type sélectionné
            plt.figure(figsize=(10, 6))

            if chart_type == 'histogram':
                sns.histplot(df[column_name], kde=False)
            elif chart_type == 'barplot':
                sns.barplot(x=df[column_name].value_counts().index, y=df[column_name].value_counts().values)
            elif chart_type == 'scatterplot':
                sns.scatterplot(x=df.index, y=df[column_name])
            elif chart_type == 'boxplot':
                sns.boxplot(x=df[column_name])
            elif chart_type == 'lineplot':
                sns.lineplot(x=df.index, y=df[column_name])

        # Sauvegarder le graphique dans un flux mémoire
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

        # Convertir en base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

            return JsonResponse({"chart": img_base64}, status=200)
    
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# Fonction get_all_columns (en dehors de la classe)
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_all_columns(request, file_id):
    try:
        file = UploadedFile.objects.get(id=file_id)  # Assure-toi de récupérer un fichier valide
        # Récupérer les colonnes du fichier
        columns = file.get_columns()  # Remplacez cette logique par celle qui récupère les colonnes réelles
        return Response(columns)
    except UploadedFile.DoesNotExist:
        return Response({"error": "Fichier introuvable"}, status=404)