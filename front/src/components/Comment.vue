<template>
  <div class="fs-4">
    <hr class="border border-danger border-2 opacity-50" />
    <form @submit.prevent="createComment">
      <div class="d-flex align-center justify-content-center">
        <label for="content"> </label>
        <input
          class="form-control"
          type="text"
          name="content"
          id="content"
          v-model="content"
        />
        <button class="ms-2 btn btn-outline-danger" type="submit">
          댓글 작성
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCommunityStore } from "@/stores/community";
import { useUserStore } from "@/stores/user";

const props = defineProps({
  reviewId: String,
});

const content = ref(null);
const store = useCommunityStore();
const userStore = useUserStore();

const createComment = function () {
  const data = {
    content: content.value,
    user: userStore.userId,
    review: props.reviewId,
  };
  store.createComment(data);
  content.value = "";
};
</script>

<style scoped>
input:focus {
  outline: 2px solid rgb(255, 0, 0);
}
.review-create-container {
  background-color: black;
  color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}
.form-group {
  margin-bottom: 15px;
}
label {
  margin-bottom: 5px;
  font-weight: bold;
}
.form-control {
  width: 40%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #333;
  color: white;
}
</style>
