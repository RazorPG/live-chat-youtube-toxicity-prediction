let interval // Untuk menyimpan ID interval

// Fungsi untuk mendapatkan live chat secara berkala
async function fetchChats(videoId) {
  try {
    const response = await fetch('/get_chats', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ video_id: videoId }),
    })

    if (!response.ok) {
      console.error('Error fetching chats:', await response.text())
      return
    }

    const chats = await response.json()
    updateChatBox(chats)
  } catch (error) {
    console.error('Error:', error)
  }
}

// Fungsi untuk memperbarui textarea dengan chat baru
function updateChatBox(chats) {
  const chatBox = document.getElementById('chat-box')
  chats.forEach(chat => {
    chatBox.value += `${chat.author}: ${chat.message} [${chat.toxicity}]\n`
  })
  chatBox.scrollTop = chatBox.scrollHeight // Gulir ke bawah otomatis
}

// Tombol Mulai Streaming
document.getElementById('start-btn').addEventListener('click', () => {
  const videoId = document.getElementById('video-id').value.trim()
  if (!videoId) {
    alert('Masukkan Video ID terlebih dahulu!')
    return
  }

  // Hentikan interval sebelumnya jika ada
  if (interval) clearInterval(interval)

  // Mulai interval untuk fetch chats setiap 5 detik
  interval = setInterval(() => fetchChats(videoId), 5000)
})
