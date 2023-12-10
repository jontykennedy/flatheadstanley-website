 const updateLocalTime = () => {
    const options = {
      dateStyle: "medium",
      timeStyle: "long",
      timeZone: 'Europe/Copenhagen'
    };
      
    const copenhagenTime = new Date().toLocaleString('en-GB', options);
    document.getElementById('localTime').innerHTML = '<b>Copenhagen, Denmark:</b> ' + copenhagenTime;
  }
  
  setInterval(updateLocalTime, 1000);
  
  updateLocalTime();
