from flask import Flask, request, render_template_string
from src.core.retriever import Retriver

def web_page(dirname):
    app = Flask(__name__)
    generator = Retriver(dirname)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>LLM Prompt Page</title>
                
                <!-- Bootstrap CSS -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {
                        background-color: #f9f9f9;
                        font-family: 'Arial', sans-serif;
                    }
                    .container {
                        margin-top: 50px;
                    }
                    textarea {
                        resize: none;
                        border: 1px solid #ccc;
                        border-radius: 8px;
                        padding: 10px;
                        font-size: 16px;
                    }
                    .btn-primary {
                        background-color: #007bff;
                        border-color: #007bff;
                        transition: all 0.3s ease;
                    }
                    .btn-primary:hover {
                        background-color: #0056b3;
                        border-color: #004990;
                    }
                    .loading-spinner {
                        display: none;
                        margin-left: 10px;
                        border: 3px solid rgba(0, 0, 0, 0.1);
                        border-top-color: #007bff;
                        border-radius: 50%;
                        width: 20px;
                        height: 20px;
                        animation: spin 1s linear infinite;
                    }
                    @keyframes spin {
                        to { transform: rotate(360deg); }
                    }
                    pre {
                        background-color: #f4f4f4;
                        padding: 10px;
                        border-radius: 8px;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    }
                </style>
            </head>
            <body>
                <div class='container'>
                    <div class='row justify-content-center'>
                        <div class='col-md-6 col-lg-6 col-sm-12 bg-white rounded shadow p-4 mb-4'>
                            <h1 class='text-center mb-4'>Enter Your Prompt:</h1>
                            <form id="promptForm" action="/" method='post' class='needs-validation' novalidate autocomplete='off'>
                                <textarea name='prompt' rows=10 cols=50 placeholder='Type your prompt here...' required></textarea><br><br>
                                <div class="d-flex justify-content-center">
                                    <button type="submit" class="btn btn-primary me-2" id="submitButton">Submit</button>
                                    <div class="loading-spinner"></div>
                                </div>
                            </form>
                            {% if result %}
                                <div class="mt-4">
                                    <h3>Result:</h3>
                                    <pre>{{ result | safe }}</pre>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Bootstrap JS and Popper.js -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
                <script>
                    document.getElementById('promptForm').addEventListener('submit', function(event) {
                        const submitButton = document.getElementById('submitButton');
                        const spinner = document.querySelector('.loading-spinner');
                        
                        // Disable button and show spinner
                        submitButton.disabled = true;
                        spinner.style.display = 'inline-block';
                        
                        // Re-enable button after form submission
                        setTimeout(function() {
                            submitButton.disabled = false;
                            spinner.style.display = 'none';
                        }, 2000); // Simulate a delay (adjust based on actual processing time)
                    });
                </script>
            </body>
            </html>
        """

        if request.method == 'POST':
            prompt = request.form.get('prompt')
            response = generator(prompt)
            return render_template_string(template, result=response)
        
        return render_template_string(template)

    return app