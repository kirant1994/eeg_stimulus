function updateImage()
    {
        obj = document.current;
        obj.src = "./images/current.png" + "?" + Math.random();
        // obj.addEventListener('error', function() { alert('Error') })
        setTimeout("updateImage()",250);
    }