const cookieBanner = document.getElementById('cookie-banner')

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookies = document.cookie.split(";");
    
    // Loop through the array elements
    for(var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].split("=");
        
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookie[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookie[1]);
        }
    }
    
    // Return null if not found
    return null;
}

if (getCookie('cookies_policy')) {
    cookieBanner.setAttribute("hidden", true)
}

document.getElementById('accept-cookies').addEventListener('click', function() {
    document.cookie = "cookies_policy={\"functional\": \"yes\"}; max-age=31557600; path=/; secure"
    cookieBanner.setAttribute("hidden", true)
});
document.getElementById('reject-cookies').addEventListener('click', function() {
    document.cookie = "cookies_policy={\"functional\": \"no\"}; max-age=31557600; path=/; secure"
    document.cookie = "remember_token=; max-age=0"
    cookieBanner.setAttribute("hidden", true)
});