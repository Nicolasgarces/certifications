from rest_framework import viewsets
from rest_framework.decorators import action
from .serializer import EmployeeSerializer
from .models import Employee
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image, Spacer
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, black
from io import BytesIO
from django.http import HttpResponse
from num2words import num2words
from babel.dates import format_date, format_datetime, format_time
import locale

class EmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def add_watermark(self, canvas, doc):
        # Ruta local de la imagen que se utilizará como marca de agua
        logo_path = 'images/cropped-turri.png'

        try:
            logo = ImageReader(logo_path)

            # Obtener el tamaño del canvas para centrar la imagen
            page_width, page_height = doc.pagesize

            # Guardar el estado actual del canvas
            canvas.saveState()

            # Configurar la transparencia
            canvas.setFillColor(Color(1, 1, 1, alpha=0.3))

            # Trasladar el canvas al centro de la página para rotar la imagen
            canvas.translate(page_width / 2.0, page_height / 2.0)

            # Rotar el canvas en 45 grados
            canvas.rotate(45)

            # Dibujar la imagen en diagonal desde el centro de la página
            canvas.drawImage(logo, -page_width / 2.0, -page_height / 2.0,
                             width=page_width, height=page_height,
                             preserveAspectRatio=True, mask='auto')

            # Restaurar el estado del canvas
            canvas.restoreState()
        except Exception as e:
            print(f"Error al cargar la imagen local: {e}")
            canvas.saveState()
            canvas.setFont("Helvetica", 20)
            canvas.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.5))
            canvas.drawCentredString(page_width / 2.0, page_height / 2.0, "Error: No se pudo cargar la marca de agua")
            canvas.restoreState()

    @action(detail=True, methods=['get'])
    def generate_certificate(self, request, pk=None):
        employee = self.get_object()
        salary_string = num2words(employee.salary, lang='es')
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        Story = []
        styles = getSampleStyleSheet()

        # Definir un nuevo estilo para el título centrado
        centered_title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading1'],
            alignment=1,
            fontSize=14,
            spaceAfter=12
        )

        # Ruta local de la imagen del logo
        logo_path = 'images/cropped-turri.png'

        try:
            logo = Image(logo_path, width=2 * inch, height=1 * inch)
            Story.append(logo)
        except Exception as e:
            print(f"Error al cargar el logo local: {e}")
            Story.append(Paragraph("Error: No se pudo cargar el logo", styles['BodyText']))

        Story.append(Spacer(1, 12))

        # Título centrado
        title = Paragraph("CERTIFICA QUE", centered_title_style)
        Story.append(title)

        # Información del empleado
        employee_info = f"""
        <b>{employee.name}</b>, identificado(a) con cédula de ciudadanía
        <b>{employee.id_number}</b> de <b>{employee.city}</b>, se encuentra vinculado mediante contrato a
        término indefinido, como {employee.position}, desde el <b>{format_date(employee.start_date, 'd ' 'MMMM ' 'YYYY', locale='es')}</b> 
        hasta la fecha, devengando un salario mensual de {salary_string} Pesos Mcte.
        <b>(${employee.salary:,.2f})</b>, más auxilio de transporte.
        """
        Story.append(Paragraph(employee_info, styles['BodyText']))

        Story.append(Spacer(1, 12))

        # Funciones
        Story.append(Paragraph("Dentro de las funciones están:", styles['Heading2']))
        functions = [
            "Trabajar con las responsabilidades asignadas por el director de proyectos, acorde al nivel de servicio.",
            "Realizar el mantenimiento preventivo, correctivo, sobre las tablas, códigos fuentes y demás, para garantizar la continuidad de la operación, previa asignación de las actividades.",
            "Garantizar que todos los ajustes que realice, cumplan con los estándares establecidos en la empresa para su posterior implementación.",
            "Cumplir con las normas y procedimientos adoptados por la empresa para el buen desarrollo de sus funciones y actividades.",
            "Tener la disposición y facilidad de desplazarse por el territorio nacional, cuando se requiera.",
            "Guardar absoluta confidencialidad y reserva con la documentación, aplicaciones y demás que maneje la empresa.",
            "Ejercer las demás funciones que le sean asignadas por el superior inmediato, de acuerdo a la naturaleza del cargo para el cumplimiento efectivo y oportuno."
        ]
        for function in functions:
            Story.append(Paragraph(f"• {function}", styles['BodyText']))

        Story.append(Spacer(1, 12))

        # Pie de página
        footer = f"""
        <para>
        Se expide a solicitud de la interesado(a), a los <b>{format_date(employee.expedition_date, 'd', locale='es')}</b> días del mes de
        <b>{format_date(employee.expedition_date, 'MMMM', locale='es')}</b> del <b>{employee.expedition_date.year}</b>.
        </para>
        """
        Story.append(Paragraph(footer, styles['BodyText']))

        Story.append(Spacer(1, 48))

        # Firma y datos de contacto
        signature = """
        <b>Atte.:</b><br/>
        <b>EVELIO TURRIAGO MURILLO</b><br/>
        Gerente
        """
        Story.append(Paragraph(signature, styles['BodyText']))

        Story.append(Spacer(1, 24))

        # Nota de verificación
        verification = "<b>Nota: Para confirmar su contenido se debe comunicar al 3164307996</b>"
        Story.append(Paragraph(verification, styles['BodyText']))

        Story.append(Spacer(1, 50))

        # Dirección y contacto en el pie de página
        contact_info = """
        Dirección: Centro Comercial Combeima Oficinas 602, 604, 608, 609, 610, 711 – Ibagué, Tolima<br/>
        Celular: +57 3164307996 – PBX +57 (8) 2770987 – 2625884 – 2620186<br/>
        soporte@turrisystem.com
        """
        Story.append(Paragraph(contact_info, styles['BodyText']))

        # Construir el documento con la marca de agua
        doc.build(Story, onFirstPage=self.add_watermark, onLaterPages=self.add_watermark)

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
