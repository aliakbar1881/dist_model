from src import socketio, app

def main():
    socketio.run(app, host='0.0.0.0', port=3030, debug=True)


if __name__ == "__main__":
    main()