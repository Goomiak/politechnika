from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.template import loader
from django.http import JsonResponse
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

matplotlib.use('Agg')

# Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='your_secret_key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['./templates'],
        },
    ],
    STATIC_URL='/static/',
)

# Views
def home(request):
    return render(request, 'home.html')

def text_page(request):
    return render(request, 'text.html')

def image_page(request):
    return render(request, 'image.html')

def video_page(request):
    return render(request, 'video.html')

def chart_page(request):
    # Generate an interactive chart
    x = range(1, 10)
    y = [i**2 for i in x]
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title('Interactive Chart')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'chart.html', {'chart': image_base64})

def dynamic_chart(request):
    # Pobierz dane wejściowe z parametrów GET (np. wartość suwaka)
    param = float(request.GET.get('param', 1))  # Domyślna wartość = 1

    # Generuj dane dla wykresu
    x = list(range(1, 11))
    y = [i * param for i in x]  # Przykład zależności y = x * param

    # Zwróć dane w formacie JSON
    return JsonResponse({'x': x, 'y': y})

# URLs
urlpatterns = [
    path('', home, name='home'),
    path('text/', text_page, name='text_page'),
    path('image/', image_page, name='image_page'),
    path('video/', video_page, name='video_page'),
    path('chart/', chart_page, name='chart_page'),
    path('chart-data/', dynamic_chart, name='dynamic_chart'),  # Nowy endpoint
]

# WSGI application
application = get_wsgi_application()

# Template files
TEMPLATES = {
    'home.html': """
    <!DOCTYPE html>
    <html>
    <head><title>Aplikacja edukacyjna</title></head>
    <body>
        <h1>Aplikacja edukacyjna</h1>
        <ul>
            <li><a href='/text/'>Text Content</a></li>
            <li><a href='/image/'>Image Content</a></li>
            <li><a href='/video/'>Video Content</a></li>
            <li><a href='/chart/'>Interactive Chart</a></li>
        </ul>
    </body>
    </html>
    """,
    'text.html': """
    <!DOCTYPE html>
    <html>
    <head><title>Text Content</title></head>
    <body>
        <h1>Text Content</h1>
        <p>This is an educational text content page.</p>
        <a href='/'>Back to Home</a>
    </body>
    </html>
    """,
    'image.html': """
    <!DOCTYPE html>
    <html>
    <head><title>Image Content</title></head>
    <body>
        <h1>Image Content</h1>
        <img src='https://via.placeholder.com/600x400' alt='Sample Image'>
        <a href='/'>Back to Home</a>
    </body>
    </html>
    """,
    'video.html': """
    <!DOCTYPE html>
    <html>
    <head><title>Video Content</title></head>
    <body>
        <h1>Video Content</h1>
        <video width='600' controls>
            <source src='https://samplelib.com/lib/preview/mp4/sample-5s.mp4' type='video/mp4'>
            Your browser does not support the video tag.
        </video>
        <a href='/'>Back to Home</a>
    </body>
    </html>
    """,
    'chart.html': """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interaktywny Wykres</title>
        <script src="https://cdn.plot.ly/plotly-2.16.1.min.js"></script>
    </head>
    <body>
        <h1>Interaktywny Wykres</h1>

        <!-- Suwak do zmiany wartości parametru -->
        <label for="param-slider">Zmień parametr:</label>
        <input type="range" id="param-slider" min="1" max="10" step="0.5" value="1">
        <span id="param-value">1</span>

        <!-- Kontener na wykres -->
        <div id="chart"></div>

        <script>
            const slider = document.getElementById('param-slider');
            const paramValue = document.getElementById('param-value');
            const chartDiv = document.getElementById('chart');

            // Funkcja do aktualizacji wykresu
            async function updateChart(param) {
                // Pobierz dane z widoku Django
                const response = await fetch(`/chart-data/?param=${param}`);
                const data = await response.json();

                // Aktualizuj wykres
                const trace = {
                    x: data.x,
                    y: data.y,
                    mode: 'lines+markers',
                    type: 'scatter'
                };

                Plotly.newPlot(chartDiv, [trace]);
            }

            // Obsługa zmiany wartości suwaka
            slider.addEventListener('input', (event) => {
                const param = event.target.value;
                paramValue.textContent = param;  // Wyświetl wartość suwaka
                updateChart(param);  // Zaktualizuj wykres
            });

            // Inicjalizacja wykresu
            updateChart(slider.value);
        </script>
    </body>
    </html>

    """,
}

# Save templates to files
import os
os.makedirs('templates', exist_ok=True)
for name, content in TEMPLATES.items():
    with open(f'templates/{name}', 'w') as f:
        f.write(content)

# Run server
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    import sys

    execute_from_command_line(sys.argv)
