const complexitySlider = document.getElementById('password-complexity');
const complexityValue = document.getElementById('complexity-value');

complexitySlider.addEventListener('input', () => {
    complexityValue.textContent = `${complexitySlider.value} characters`;
});

function getPasswords() {
    return JSON.parse(localStorage.getItem('passwords')) || [];
}

function savePasswords(passwords) {
    localStorage.setItem('passwords', JSON.stringify(passwords));
}

function copyToClipboard(password) {
    navigator.clipboard.writeText(password).then(() => {
        console.log('copied');
    });
}

function generatePassword() { 
    const complexity = document.getElementById('password-complexity').value;

    const randomPassword = window.crypto.getRandomValues(new BigUint64Array(4)).reduce(
        (prev, curr, index) => (
            !index ? prev : prev.toString(36)
        ) + (
            index % 2 ? curr.toString(36).toUpperCase() : curr.toString(36)
        )
    ).slice(-complexity);;

    document.getElementById('password').value = randomPassword;
}

function deletePassword(index) {
    const passwords = getPasswords();
    passwords.splice(index, 1);
    savePasswords(passwords);
    displayPasswords();
}

function savePassword() {
    const site = document.getElementById('site').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!site || !username || !password) {
        alert('All fields are required!');
        return;
    }

    const passwords = getPasswords();
    passwords.push({ site, username, password });
    savePasswords(passwords);
    displayPasswords();

    document.getElementById('password-form').reset();
}

function displayPasswords() {
    const passwords = getPasswords();
    const tableBody = document.querySelector('#password-body');
    tableBody.innerHTML = '';

    passwords.forEach((item, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <a href="${item.site}" target="_blank"> 
                    ${item.site}
                </a>
            </td>
            <td>${item.username}</td>
            <td><span class="password">${item.password}</span></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="copyToClipboard(${item.password})">
                    <i class="bi bi-clipboard"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deletePassword(${index})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

displayPasswords();