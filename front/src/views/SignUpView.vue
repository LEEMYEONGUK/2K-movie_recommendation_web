<template>
  <div class="signup-container font">
    <h1 class="font">회원가입 페이지</h1>
    <form ref="form" @submit.prevent="signup" class="'signup-form'">
      <div class="form-group">
        <input type="text" id="username" name="username" placeholder="nickname을 입력하세요."/>
      </div>

      <div class="form-group">
        <input type="password" id="password1" name="password1" placeholder="password를 입력하세요."/>
      </div>

      <div class="form-group">
        <input type="password" id="password2" name="password2" placeholder="password를 한 번 더 입력하세요." />
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

const signup = function () {
  const data = new FormData(form.value);
  const username = data.get("username");
  const password1 = data.get("password1");
  const password2 = data.get("password2");

  if (!username || !password1 || !password2) {
    alert("작성되지 않은 항목이 있습니다.");
    return;
  }

  if (password1 !== password2) {
    alert("비밀번호와 비밀번호 확인이 같지 않습니다.");
    return;
  }

  if (password1.length < 8) {
    alert("비밀번호가 너무 짧습니다.");
    return;
  }

  store.signup(data);
  form.value.reset();
  router.push({ name: "login" });
};
</script>

<style scoped>
.signup-container {
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

.signup-form {
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
  background-color: #4caf50;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
