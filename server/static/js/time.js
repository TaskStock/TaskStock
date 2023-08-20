window.onload = async function() {
    let timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    try {
        const response = await fetch('/main/set_timezone/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //CSRF 토큰 추가
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ timezone: timezone })
        });

        const data = await response.json();
        // console.log(data.status);
    } catch (error) {
        console.error("Error sending timezone:", error);
    }
}

// Django의 CSRF 토큰을 가져오는 함수
function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
