export function playSound() {
  const audio = new Audio('/sounds/GolfCup.mp3')
  console.log('Audio wird abgespielt' + audio.src)
  audio.currentTime = 7.5 // Start von Anfang
  audio.play().catch((error) => {
    console.error('Audio konnte nicht abgespielt werden:', error)
  })
  setTimeout(() => {
    audio.pause() // Stoppt die Wiedergabe
    audio.currentTime = 0 // Setzt den Sound zurück auf den Anfang
  }, 1000)
}
const audioGolf = new Audio('/sounds/GolfMusic.mp3')

export function playGolfMusic() {
  audioGolf.currentTime // Start von Anfang
  audioGolf.play().catch((error) => {
    console.error('Audio konnte nicht abgespielt werden:', error)
  })
  audioGolf.loop = true
}

export function stopGolfMusic() {
  audioGolf.pause() // Stoppt die Wiedergabe
}
