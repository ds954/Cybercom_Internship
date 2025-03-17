async function fetchWithAuth(url, options = {}) {
    let accessToken = getCookie('access_token');

    if (!options.headers) {
        options.headers = {};
    }

    // Add Authorization header
    options.headers['Authorization'] = `Bearer ${accessToken}`;

    let response = await fetch(url, options);

    if (response.status === 401) {
        console.log("Access token expired. Attempting refresh...");

        const refreshSuccess = await refreshAccessToken();
        if (refreshSuccess) {
            accessToken = getCookie('access_token');
            options.headers['Authorization'] = `Bearer ${accessToken}`;
            response = await fetch(url, options);
        } else {
            window.location.href = "/login/";
            return;
        }
    }

    return response;
}

async function refreshAccessToken() {
    try {
        const response = await fetch('/refresh-token/', {
            method: 'POST',
            credentials: 'include'
        });

        if (!response.ok) {
            window.location.href = "/login/";
            return false;
        }

        return true;
    } catch (error) {
        window.location.href = "/login/";
        return false;
    }
}

function getCookie(name) {
    let match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? match.pop() : '';
}
