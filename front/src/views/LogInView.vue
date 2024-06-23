<template>
  <div class="login-container">
    <h1 class="font">로그인 페이지</h1>
    <form ref="form" @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">username : </label>
        <input type="text" name="username" id="username" v-model="username" />
      </div>

      <div class="form-group">
        <label for="password">password : </label>
        <input type="password" name="password" id="password" />
      </div>

      <button type="submit">submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";

const form = ref(null);
const router = useRouter();
const store = useUserStore();
const username = ref("");

const login =  async function () {
  if (!username.value || !password.value) {
    alert('입력되지 않은 항목이 있습니다.');
    return;
  }

  const data = new FormData(form.value);

  const isLogin = await store.login(data, username);

  if (isLogin) {
    form.value.reset();
    router.push({ name: "home" });
  } else {
    alert("아이디와 비밀번호를 다시 확인해주세요");
  }
};

</script>

<style scoped>
.login-container {
  background-color: black;
  color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  margin: 0 auto;
  box-shadow: 0 14px 28px rgba(44, 44, 44, 0.25), 0 10px 10px rgba(15, 15, 15, 0.22);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  margin-bottom: 5px;
  font-weight: 900;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #333;
  color: white;
}

button {
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #4CAF50;
  /* background-color: #d32d3e; */
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
  /* background-color: #d61428; */
}
</style>
