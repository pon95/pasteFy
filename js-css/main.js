const initApp = () => {
    const droparea = document.querySelector('.droparea');

    const active = () => {droparea.classList.add("green-border");
                          droparea.classList.remove('no-border');
    }

    const inactive = () => {droparea.classList.remove("green-border");
                            droparea.classList.add('no-border');
    };

    const prevents = (e) => e.preventDefault();

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evtName => {
            droparea.addEventListener(evtName, prevents);
    });

    ['dragenter', 'dragover'].forEach(evtName => {
        droparea.addEventListener(evtName, active);
    });

    ['dragleave', 'drop'].forEach(evtName => {
        droparea.addEventListener(evtName, inactive);
    });

    droparea.addEventListener('drop', handleDrop);
}

document.addEventListener("DOMContentLoaded", initApp)

const handleDrop = (e) => {
    const textInput = document.getElementById('auto-resize-textarea');
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        const file = files[0];

        if (file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
            // Если это .docx файл, вызываем функцию для его обработки
            readDocxFile(file);
        } else  {
            // Если это текстовый файл (.txt), обрабатываем его с помощью FileReader
            const reader = new FileReader();
            reader.onload = function () {
                textInput.value += reader.result;
            };
            reader.readAsText(file);
        } 
    }
}
fileInput.addEventListener('change', readDocxFile(fileInput.files[0]))
function readDocxFile(file) {
    var textarea = document.getElementById('auto-resize-textarea');
    var convertedContent = document.getElementById('converted-content');
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var arrayBuffer = e.target.result;
            mammoth.convertToHtml({ arrayBuffer: arrayBuffer })
                .then(displayResult)
                .catch(handleError);
        };
        reader.readAsArrayBuffer(file);
    }

    function displayResult(result) {
        convertedContent.innerHTML = result.value;
    }

    function handleError(err) {
        console.error(err);
        textarea.value = 'Произошла ошибка при чтении файла.';
    }
}