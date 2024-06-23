<template>
  <div class="home">
    <div class="overlay">
      <header class="header">
        <img class="logo" src="@/assets/site_logo.png">
        <div class="nav">
          <div class="nav-item"><RouterLink :to="{ name:'home'}">홈</RouterLink></div>
          <div class="nav-item"><RouterLink :to="{ name:'list'}">영화</RouterLink></div>
          <div class="nav-item"><RouterLink :to="{ name:'community'}">커뮤니티</RouterLink></div>
        </div>
        <div class="menu">
          <div class="search">
            <i class="bi bi-search" style="color: #ffffff;" @click="openSearchModal"></i>
          </div>
          <div v-if="!store.isLogin">
            <RouterLink :to="{ name:'signup'}" style="padding-right: 40px;">회원가입</RouterLink>
            <RouterLink :to="{ name:'login'}">로그인</RouterLink>
          </div>
          <div v-else>
            <a @click="logout" style="padding: 20px;  cursor: pointer;">로그아웃</a>
            <RouterLink :to="{ name:'profile'}">프로필</RouterLink>
            <div class="Chat">
              <i class="bi bi-chat-right-quote-fill text-red" @click="openChatModal"></i>
            </div>
          </div>
        </div>
      </header>
      <div v-if="isSearchModalOpen" class="modal-overlay" @click.self="closeSearchModal">
        <div class="modal-content">
          <div>
            <button class="close-button" @click="closeSearchModal"><i class="bi bi-x-circle-fill"></i></button>
          </div>
          <div>
            <SearchModal @close="closeSearchModal" :close-modal="closeSearchModal" /> 
          </div>
        </div>
      </div>
      <div v-if="isChatModalOpen" class="modal-overlay-chat" @click.self="closeChatModal">
        <div class="modal-content-chat">
          <div>
            <button class="close-chat" @click="closeChatModal"><i class="bi bi-x-circle-fill"></i></button>
          </div>
          <div>
            <chatbot @close="closeChatModal" :close-modal="closeChatModal" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <RouterView/>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
import SearchModal from '@/components/SearchModal.vue';
import chatbot from '@/components/chatbot.vue';

const store = useUserStore()
const router = useRouter()
const isSearchModalOpen = ref(false)
const isChatModalOpen = ref(false)

const logout = function () {
  store.logout()
  router.push({ name: 'login' })
}

const openSearchModal = () => {
  isSearchModalOpen.value = true
}

const closeSearchModal = () => {
  isSearchModalOpen.value = false
}

const openChatModal = () => {
  isChatModalOpen.value = true
}

const closeChatModal = () => {
  isChatModalOpen.value = false
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  background-color: black;
  padding: 10px 50px;
  position: fixed; /* 네비게이션 바 고정 */
  width: 100%; /* 전체 폭 차지 */
  top: 0; /* 상단에 고정 */
  z-index: 1000; /* 다른 요소들 위에 위치 */
}
a {
  text-decoration-line: none;
  color: #ffffff;
}
.logo {
  height: 50px;
  margin-right: 40px;
}

.nav {
  display: flex;
  flex-grow: 1;
  color: white;
  font-size: 18px;
}

.nav-item {
  padding: 0 20px;
}

.menu {
  display: flex;
  align-items: center;
  color: white;
}

.menu-item {
  padding: 10px;
}

.menu .search {
  padding-right: 30px;
  cursor: pointer;
}

.profile {
  margin-left: 20px;
  height: 40px;
  width: 40px;
  border-radius: 10px;
}
.home {
  background-color: black; /* 배경을 검정색으로 설정 */
  padding-top: 80px; /* 네비게이션 바 공간 확보 */
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 상단에 정렬 */
  z-index: 1100; /* 네비게이션 바 위에 위치 */
}

.modal-overlay-chat {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end; /* 우측 하단에 정렬 */
  align-items: flex-end; /* 우측 하단에 정렬 */
  z-index: 1100; /* 네비게이션 바 위에 위치 */
}

.modal-content {
  background-color: rgb(0, 0, 0);
  padding: 10px;
  border-radius: 3px;
  width: 80%;
  max-width: 600px;
  max-height: 80%;
  overflow-y: auto;
  position: relative;
}

.modal-content-chat {
  background-color: rgb(0, 0, 0);
  padding: 10px;
  border-radius: 3px;
  width: 600px; /* 원하는 너비로 수정 */
  max-height: 500px;
  overflow-y: auto;
  position: relative;
  margin: 20px; /* 모달과 화면 가장자리 사이의 간격 */
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 1200; /* z-index 추가 */
}

.close-chat {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: red;
  z-index: 1200; /* z-index 추가 */
}

.Chat{
  position: fixed;
  bottom: 30px;
  right: 50px;
  font-size: xx-large;
  cursor: pointer;
}
</style>
