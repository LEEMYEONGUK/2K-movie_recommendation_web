<template>
  <div class="d-flex align-items-center justify-content-center fs-6">
    <p class="mb-0">
      {{ comment.content }}
      
    </p>
    <div class="buttons-container">
      <button @click="commentLike()" class="like-button">
        <span class="badge" v-if="commentLikeCount > 0">{{ commentLikeCount }}</span>
        <i class="bi bi-hand-thumbs-up-fill icon-color" v-if="commentLiked"></i>
        <i class="bi bi-hand-thumbs-up icon-color" v-else></i>

      </button>
      <button @click="commentHate()" class="hate-button">
        <span class="badge" v-if="commentHateCount > 0">{{ commentHateCount }}</span>
        <i class="bi bi-hand-thumbs-down-fill icon-color" v-if="commentHated"></i>
        <i class="bi bi-hand-thumbs-down icon-color" v-else></i>
      </button>
      <div v-if="store.userId === comment.user">
        <button @click="commentDelete(comment.review, comment.id)">
          <i class="bi bi-trash trash"></i>
        </button>
      </div>
    </div>
  </div>
  <hr class="border border-danger border-2 opacity-30">

</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useCommunityStore } from '@/stores/community'
import axios from "axios";

const props = defineProps({
  comment: Object,
})

const commentLiked = ref(false);
const commentHated = ref(false);
const commentLikeCount = ref(0);
const commentHateCount = ref(0);

const store = useUserStore()
const communityStore = useCommunityStore()

const commentDelete = function (commentReview, commentId) {
  axios({
    method: "delete",
    url: `http://127.0.0.1:8000/api/v1_1/${commentReview}/comment/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      console.log("코멘트 삭제 완료");
      communityStore.getComments(commentReview)
      router.push({name:'reviewDetail', params:{reviewId:commentReview}})
    })
    .catch((error) => {
      console.log(error);
    });
}

const commentLike = function () {
  axios({
    method: "post",
    url: `http://127.0.0.1:8000/api/v1_1/${props.comment.review}/comment/${props.comment.id}/like/${props.comment.user}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response)
      commentLiked.value = response.data.liked
      commentLikeCount.value = response.data.count
      console.log("코멘트 좋아요 완료")
    })
    .catch((error) => {
      console.log(error)
    });
};

const commentHate = function () {
  axios({
    method: "post",
    url: `http://127.0.0.1:8000/api/v1_1/${props.comment.review}/comment/${props.comment.id}/hate/${props.comment.user}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response)
      commentHated.value = response.data.hated
      commentHateCount.value = response.data.count
      console.log("코멘트 싫어요 완료");
    })
    .catch((error) => {
      console.log(error)
    });
};

onMounted(() => {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1_1/${props.comment.review}/comment/${props.comment.id}/like/${props.comment.user}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response)
      commentLiked.value = response.data.liked
      commentLikeCount.value = response.data.count
      console.log("코멘트 좋아요 조회 완료")
    })
    .catch((error) => {
      console.log(error)
    })
    
    axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1_1/${props.comment.review}/comment/${props.comment.id}/hate/${props.comment.user}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response)
      commentHated.value = response.data.hated
      commentHateCount.value = response.data.count
      console.log("코멘트 싫어요 조회 완료");
    })
    .catch((error) => {
      console.log(error)
    })
})

</script>

<style scoped>
.trash {
  font-size: 20px;
  color:red;
}
.icon-color {
  font-size: 20px;
  color: white;
}
.text-color {
  font-size: 15px;
  font-weight: 900;
  color: white;
}

.buttons-container {
  display: flex;
  align-items: center;
}

button {
  position: relative;
  padding: 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
}

.like-button, .hate-button {
  margin-right: 20px;
}

.badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: red;
  color: white;
  border-radius: 30%;
  padding: 5px 10px;
  font-size: 20px;
  display: inline-block;
}
</style>
