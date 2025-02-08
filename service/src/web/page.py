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
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
                
            </head>

            <body style='background-color:#f9f9f9;'>
                
            <div class='container mt-5'>
                    <div class='row justify-content-center'>
                        <div class='col-md-6 col-lg-6 col-sm-12 bg-light rounded shadow p-4 mb-4'>
                            <h1 class='text-center'>Enter Your Prompt:</h1><br><br>

                            <!-- Form with bootstrap classes applied -->
                            <form action="/" method='post' class='needs-validation' novalidate autocomplete='off'>

                                <!-- Textarea with bootstrap styling -->
                                <textarea name='prompt' rows=10 cols=50 placeholder='' required></textarea><br><br>

                                <!-- Submit button styled using bootstrap classes -->
                                {% if result %}
                                    &nbsp;<button type=submit disabled style=color:white;background-color:#007bff;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px;border-radius :5%;border-style:none;cursor:pointer;transition-duration :0.4s ;transition-property :background-color >Submit Again!</button>&nbsp;
                                    &nbsp;<input type=submit value=Submit style=color:white;background-color:#007bff;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px;border-radius :5%;border-style:none;cursor:pointer;transition-duration :0.4s ;transition-property :background-color >
                                
                                {% else %}
                                    &nbsp;<input type=submit value=Submit style=color:white;background-color:#007bff;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px;border-radius :5%;border-style:none;cursor:pointer;transition-duration :0.4s ;transition-property :background-color >
                                
                                {% endif %}

                            </form>

                            
                            {% if result %}
                            
                                <h3>Result:</h3> 
                                <pre>{{ result | safe }}</pre> 
                            {% endif %} 

                        </div>	
                    </div>	
                    
                </div>

            <!-- Optional JavaScript for additional functionality (not needed here)-->
            <script src=https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js integrity sha384 kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4 crossorigin anonymous></script>

            </body></html>
        """
        if request.method == 'POST':
            prompt = request.form.get('prompt')

            response = generator(prompt)            
            return render_template_string(template, result=response)
        
        return render_template_string(template)
    return app
