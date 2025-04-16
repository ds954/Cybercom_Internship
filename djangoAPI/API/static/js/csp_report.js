// This JavaScript sends a POST request to your /csp-report/ API endpoint
fetch("https://127.0.0.1:8000/user/csp-report/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        
    },
    body: JSON.stringify({
        csp_report: {
            "document-uri": "http://localhost:8000.com",
            "referrer": "",
            "violated-directive": "default-src self",
            "original-policy": "default-src self; report-uri /csp-report/",
            "blocked-uri": "http://evil.com/script.js"
        }
    })
})
.then(response => {
    if (response.ok) {
        return response.json();  // Parse the response as JSON
    }
    throw new Error('Failed to send CSP report');
})
.then(data => {
    console.log('CSP report sent successfully:', data);
})
.catch(error => {
    console.error('Error sending CSP report:', error);
});
