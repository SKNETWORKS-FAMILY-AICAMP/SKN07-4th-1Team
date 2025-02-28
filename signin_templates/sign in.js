document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.querySelector('#username').value;
        const password = document.querySelector('#password').value;

        // 기본적인 유효성 검사를 수행합니다.
        if (username.trim() === '' || password.trim() === '') {
            alert('아이디와 비밀번호를 입력해 주세요.');
            return;
        }

        // 서버로 데이터를 전송하는 부분
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('회원가입에 성공했습니다!');
            } else {
                alert('오류가 발생했습니다. 다시 시도해 주세요.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('서버와 통신하는 중 오류가 발생했습니다.');
        });
    });

    // CSRF 토큰을 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
