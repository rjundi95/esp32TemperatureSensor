'''
Thread 2
    -Cria o server atraves do metodo socket()
    -Decodifica os arquivos em html, js, css para criar um web
    -Puxa os dados do csv para criar o grafico na web

'''
import network
import globals 

def handle_client(client_socket):
    """Handles incoming client requests."""
    try:
        request = client_socket.recv(1024).decode()
        print("Request received:", request)

        response = "HTTP/1.1 404 Not Found\n\n"

        if "GET / " in request or "GET /index.html" in request:
            html = load_file("index.html")
            if html:
                response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html

        elif "GET /script.js" in request:
            js = load_file("script.js")
            if js:
                response = "HTTP/1.1 200 OK\nContent-Type: application/javascript\n\n" + js

        elif "GET /style.css" in request:
            css = load_file("style.css")
            if css:
                response = "HTTP/1.1 200 OK\nContent-Type: text/css\n\n" + css

        elif "GET /data" in request:
            try:
                csv_data = load_file("data.csv")
                response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\n" + csv_data
            except Exception as e:
                response = "HTTP/1.1 500 Internal Server Error\n\nError reading CSV file"
                globals.led_error_internet()
        client_socket.send(response.encode())  # send response
        
    except OSError as e:
        if e.errno == errno.ECONNRESET:
            print("Connection reset by peer (client disconnected abruptly)")
            globals.led_error_internet()
        else:
            print(f"Unexpected error: {e}")
            globals.led_error_internet()
    finally:
        client_socket.close()  # Ensure the socket is closed properly    
    

# Carrega o arquivo no metodo do os
def load_file(filename):
    """Loads a file from the ESP32 filesystem."""
    try:
        with open(filename, "r") as file:  # Open the file in read mode
            arquivo = file.read()
            return arquivo  # Read and return file content
    except:
        return None  # Return None if the file is missing or an error occurs
        globals.led_error_internet()

# Carrega o arquivo html
def load_html():
    """Loads HTML file."""
    try:
        with open("index.html", "r") as file:
            return file.read()
    except Exception as e:
        print("Error loading HTML:", e)
        globals.led_error_internet()
        return "<h1>Error loading page</h1>"
