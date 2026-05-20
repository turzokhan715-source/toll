try:
        data = request.get_json() or {}
        raw_input = data.get('raw_input', '').strip()

        if not raw_input:
            response = jsonify({'status': 'error', 'message': 'Input empty.'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        detected_email = extract_email_from_string(raw_input)
        if not detected_email:
            response = jsonify({'status': 'error', 'message': 'No valid email found in data.'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        # Split correctly using pipe
        parts = [p.strip() for p in raw_input.split('|') if p.strip()]
        
        if len(parts) < 3:
            response = jsonify({'status': 'error', 'message': 'Format must be email|pass|token'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        email = detected_email
        password = parts[1]
        refresh_token = parts[2]
        
        # Jodi input-e client_id (4th part) na thake, tobe standard fallback use korbe
        if len(parts) >= 4:
            client_id = parts[3]
        else:
            # Common Microsoft Outlook/Graph Native Client ID
            client_id = "f1e6c35b-1634-4bc0-b53d-24e526d140e6" 

        # API-te data pathano
        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        if fb_code.isdigit():
            response = jsonify({
                'status': 'success', 
                'email': email, 
                'code': fb_code
            })
        else:
            response = jsonify({
                'status': 'error', 
                'message': fb_code
            })
            
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except Exception as e:
        # Error track korar jonno print/log hobe
        print(f"CRITICAL ERROR: {str(e)}") 
        response = jsonify({'status': 'error', 'message': f"Server error: {str(e)}"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500
