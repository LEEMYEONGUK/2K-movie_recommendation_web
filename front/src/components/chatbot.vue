<template>
  <div>
      <!-- 채팅창 화면 -->
      <section class="container">
          <!-- 프로필 영역 -->
          <div class="top-area">
              <div class="profile-area">
                  <span>Jarvis</span>
              </div>
          </div>
          <!-- 채팅 영역 -->
          <div class="chat-area" ref="chatContainer">
              <div v-if="showInitialMessage" class="chat receive-chat" style="
          background-color: #1f1f1f;
          align-self: flex-start;
          margin-right: auto;
          border-radius: 30px;
          padding: 5px 15px;
          box-sizing: border-box;
          color: white;
          width: fit-content;
          max-width: 70%;
          height: fit-content;
          word-break: break-all;
          margin: 5px 0; 
          ">안녕하세요, 궁금하신 영화 정보를 여쭤보세요</div>


          </div>
          <!-- 채팅창 하단 영역 -->
          <div class="bottom-area">
              <input class="chat-input" type="text" placeholder="영화 관련 정보를 여쭤보세요!" v-model="message"
                  @keyup.enter="chatSubmit" />
          </div>
      </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 메시지 상태 관리
const message = ref('')
const chatContainer = ref(null)

// 초기 메시지 표시 상태 관리
const showInitialMessage = ref(false)

// API URL 및 키
const OPEN_API_URL = 'https://api.openai.com/v1/chat/completions'
const API_KEY = process.env.VUE_APP_API_KEY

// 필요한 헤더 정보
const headers = {
  Authorization: `Bearer ${API_KEY}`, // 인증 키 설정
  'Content-Type': 'application/json' // 요청 데이터의 타입
}

// 대화 내용을 저장하는 배열
const chatHistory = ref([])

// 초기 시스템 메시지 추가 (수정 부분)
chatHistory.value.push({
  role: 'system',
  content: '넌 이제부터 영화 전문가야. 영화 관련 정보를 물어보면 자세히 대답해줘'
})

// 채팅창에 내용을 추가해주는 부분
const addChat = (type, value) => {
  const chat = document.createElement('div')
  chat.classList.add('chat')
  chat.innerText = value
  chat.classList.add(`${type}-chat`)
  if (type === 'send') {
      chat.style.cssText = `
          background-color: #FF0000;
          align-self: flex-end;
          margin-left: auto;
          border-radius: 30px;
          padding: 5px 15px;
          box-sizing: border-box;
          color: white;
          width: fit-content;
          max-width: 70%;
          height: fit-content;
          word-break: break-all;
          margin: 5px 0; `
  } else if (type === 'receive') {
      chat.style.cssText = `
          background-color: #1f1f1f;
          align-self: flex-start;
          margin-right: auto;
          border-radius: 30px;
          padding: 5px 15px;
          box-sizing: border-box;
          color: white;
          width: fit-content;
          max-width: 70%;
          height: fit-content;
          word-break: break-all;
          margin: 5px 0; 
          `
  } chatContainer.value.appendChild(chat)
  chatContainer.value.scrollTop = chatContainer.value.scrollHeight
}

// chatGPT API 서버에 요청을 보내는 함수
const chatReceive = async (userMsg) => {
  // 사용자가 입력한 내용을 히스토리에 추가
  chatHistory.value.push({ role: 'user', content: userMsg })

  try {
      const response = await axios.post(OPEN_API_URL, {
          model: 'gpt-3.5-turbo',
          messages: chatHistory.value // 대화 히스토리를 메시지로 전송
      }, { headers })

      const receivedMsg = response.data.choices[0].message.content
      addChat('receive', receivedMsg)
      // 응답받은 내용을 히스토리에 추가
      chatHistory.value.push({ role: 'assistant', content: receivedMsg })
  } catch (error) {
      console.error(error.response.data)
      console.error(error.response.status)
  }
}

const chatSubmit = () => {
  if (!message.value) return
  addChat('send', message.value)
  chatReceive(message.value)
  message.value = ''
}

// 페이지가 로드된 후 1초 뒤에 초기 메시지 표시
onMounted(() => {
  setTimeout(() => {
      showInitialMessage.value = true
  }, 1000)
})


</script>

<style scoped>
:root {
  --color-primary: skyblue;
  --color-primary-light: skyblue;
  --color-secondary: skyblue;
  --color-chat: #e6f3f6;
  --color-white: #f9fbff;
  --color-text: #595959;
  --color-gray: #aab5b5;
}


/* 채팅 영역 */
.chat-area {
  width: 100%;
  display: flex;
  flex: 1;
  /* background-color: var(--color-chat); */
  padding: 10px;
  box-sizing: border-box;
  flex-direction: column;
  overflow-y: scroll;
}

.chat-area::-webkit-scrollbar {
  width: 10px;
  background-color: transparent;
}

.chat-area::-webkit-scrollbar-thumb {
  /* background-color: var(--color-primary-light); */
  border-radius: 10px;
}

/* 전송, 수신 채팅 공통 */
.chat {
  border-radius: 30px;
  padding: 5px 15px;
  box-sizing: border-box;
  /* color: var(--color-white); */
  width: fit-content;
  max-width: 70%;
  height: fit-content;
  word-break: break-all;
  margin: 5px 0;
}

/* 전송한 채팅 */
.send-chat {
  /* background-color: var(--color-primary); */
  align-self: flex-end;
  margin-left: auto;
}

/* 수신한 채팅 */
.receive-chat {
  /* background-color: var(--color-gray); */
  align-self: flex-start;
  margin-right: auto;
}

/* 채팅 입력 iuput */
.chat-input {
  width: 100%;
  border: none;
  font-size: 16px;
  background-color: transparent;
  color: #595959;
  ;
}

.chat-input:focus {
  outline: none;
}

.chat-input::placeholder {
  color: #aab5b5;
}

/* 프로필, 채팅, 입력창을 담는 컨테이너 */
.container {
  width: 100%;
  height: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: var(--color-white);
  border-radius: 30px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  position: relative;
}

.profile-area {
  display: flex;
  align-items: center;
}

.profile-area>span {
  margin-left: 10px;
  font-size: 20px;
  font-weight: semi-bold;
  color: var(--color-text);
}

/* 입력창, 툴 */
.bottom-area {
  width: 100%;
  height: 13%;
  display: flex;
  padding: 10px 20px;
  box-sizing: border-box;
}
.modal-overlay-chat {
  position: fixed;
  bottom: 70px; /* Fixed bottom position */
  right: 70px; /* Fixed right position */
  width: auto;
  height: auto;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 상단에 정렬 */
  z-index: 1100; /* 네비게이션 바 위에 위치 */
}
.modal-content-chat {
  background-color: rgb(0, 0, 0);
  padding: 10px;
  border-radius: 3px;
  width: 300px;
  max-height: 500px;
  overflow-y: auto;
  position: relative;
}
.tool-area {
  display: flex;
  align-items: center;
  color: var(--color-secondary);
}
</style>
