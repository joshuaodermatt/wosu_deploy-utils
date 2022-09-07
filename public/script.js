const host = 'localhost:3000'

document.getElementById('submit').addEventListener('click', () => {
    const folder = document.getElementById('folder').value.toString()
    const key = document.getElementById('key').value.toString()
    const repKey = document.getElementById('rep-key').value.toString()

    if (
        folder.trim().length > 0 &&
        key.trim().length >= 12 &&
        key === repKey
    ) {
        const data = {
            key: key,
            folder: folder
        }
        fetch('http://' + host + '/configure',
            {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(() => console.log('configured'))
    }
})
