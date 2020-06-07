padDT = function(str) {
        return String(str).padStart(2, '0')
}

updateDateTime = function() {
        let datetime = new Date()

        let formatDate = padDT(datetime.getDate()) + "/" + padDT(datetime.getMonth()) + "/" + padDT(datetime.getFullYear())
        let formatTime = padDT(datetime.getHours()) + ":" + padDT(datetime.getMinutes()) + ":" + padDT(datetime.getSeconds())

        document.getElementById("labelDate").innerHTML = formatDate
        document.getElementById("labelTime").innerHTML = formatTime
    
    update_alarms_list()
}

updateAlarmsStack = function() {
        document.getElementById("alarmsStack").innerHTML = "vandalized by innerHTLM"
}

setInterval(updateDateTime, 500)
