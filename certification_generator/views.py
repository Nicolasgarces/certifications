# from rest_framework import viewsets
# from .serializer import EmployeeSerializer
# from .models import Employee
#
#
#
# # Create your views here.
#
# class EmployeeView(viewsets.ModelViewSet):
#     serializer_class = EmployeeSerializer
#     queryset = Employee.objects.all()

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .serializer import EmployeeSerializer
from .models import Employee
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate
from io import BytesIO
from django.http import HttpResponse


class EmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    @action(detail=True, methods=['get'])
    def generate_certificate(self, request, pk=None):
        employee = self.get_object()

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        Story = []
        styles = getSampleStyleSheet()

        # Título
        title = Paragraph("CERTIFICA QUE", styles['Heading1'])
        Story.append(title)

        # Contenido principal
        content = f"""
         <para>
         {employee.name}, identificado con cédula de ciudadanía
         {employee.id_number} de {employee.city}, se encuentra vinculado mediante contrato a
         término indefinido, como {employee.position}, desde el {employee.start_date.strftime('%d de %B')}
         del año {employee.start_date.year} hasta la fecha, devengando un salario mensual de
         {employee.salary}, más auxilio de transporte.
         </para>
         """
        Story.append(Paragraph(content, styles['BodyText']))

        # Funciones
        Story.append(Paragraph("Dentro de las funciones están:", styles['Heading2']))
        functions = [
            "Trabajar con las responsabilidades asignadas por el director de proyectos, acorde al nivel de servicio.",
            "Realizar el mantenimiento preventivo, correctivo, sobre las tablas, códigos fuentes y demás, para garantizar la continuidad de la operación, previa asignación de las actividades.",
            "Garantizar que todos los ajustes que realice, cumplan con los estándares establecidos en la empresa para su posterior implementación.",
            "Cumplir con las normas y procedimientos adoptados por la empresa para el buen desarrollo de sus funciones y actividades.",
            "Tener la disposición y facilidad de desplazarse por el territorio nacional, cuando se requiera.",
            "Guardar absoluta confidencialidad y reserva con la documentación, aplicaciones y demás que maneje la empresa.",
            "Ejercer las demás funciones que le sean asignadas por el superior inmediato, de acuerdo a la naturaleza del cargo para el cumplimiento efectivo y oportuno"

            # ... (agregar el resto de las funciones)
        ]
        for function in functions:
            Story.append(Paragraph(f"• {function}", styles['BodyText']))

        # Pie de página
        footer = f"""
         <para>
         Se expide con destino a la Cooperativa Beneficiar, a los {employee.expedition_date.strftime('%d')} días del mes de
         {employee.expedition_date.strftime('%B')} del {employee.expedition_date.year}.
         </para>
         """
        Story.append(Paragraph(footer, styles['BodyText']))

        doc.build(Story)

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')