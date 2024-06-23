<template>
  <div class="post-container">
    <div class="post-header">
      <img class="profile-pic" src="@/assets/profile.jpg" alt="Profile Picture" />
      <div class="user-info">
        <p class="username">{{ review.username }}</p>
      </div>
    </div>
    <img class="post-image" :src="`https://image.tmdb.org/t/p/w500${review.poster_path}`" alt="Post Image" />
    <div class="post-actions">
      <div>
        <i class="bi bi-hand-thumbs-up-fill icon-color" @click="reviewLike()" v-if="reviewLiked"></i>
        <i class="bi bi-hand-thumbs-up icon-color" @click="reviewLike()" v-else></i>
      </div>
      <div>
        <i class="bi bi-hand-thumbs-down-fill icon-color" @click="reviewHate()" v-if="reviewHated"></i>
        <i class="bi bi-hand-thumbs-down icon-color" @click="reviewHate()" v-else></i>
      </div>
      <div v-if="review.user === store.userId" class="button-item">
        <i class="bi bi-trash trash icon-color" @click="reviewDelete" style="cursor: pointer;"></i>
      </div>
      <div v-if="review.user === store.userId">
        <i class="bi bi-pencil-square icon-color" @click="openReviewUpdateModal"></i>
      </div>
    </div>
    <div class="post-likes">
      <p>좋아요 {{ reviewLikeCount }}개&nbsp;&nbsp; 싫어요 {{ reviewHateCount }}개&nbsp;&nbsp;&nbsp;&nbsp;<i class="bi bi-star-fill star"></i>&nbsp;&nbsp;{{ review.rank }}</p>

    </div>
    <div class="post-content">
      <h2>{{ review.title }}</h2>
      <p>{{ review.content }}</p>
    </div>
    <div class="post-comments">
      <CommentList
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </div>
    <div class="">
      <Comment :review-id="reviewId" />
    </div>
    <div v-if="isReviewUpdateModalOpen" class="modal-overlay-reviewcreate" @click.self="closeReviewUpdateModal">
      <div class="modal-content-reviewcreate">
        <div>
          <button class="close-reviewcreate" @click="closeReviewUpdateModal"><i class="bi bi-x-circle-fill"></i></button>
        </div>
        <div>
          <ReviewUpdate :review="review" @close="closeReviewUpdateModal" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
import { useCommunityStore } from "@/stores/community";
import axios from "axios";
import CommentList from "@/components/CommentList.vue";
import Comment from "@/components/Comment.vue";
import ReviewUpdate from "@/components/ReviewUpdate.vue";

const store = useUserStore();
const communityStore = useCommunityStore();
const isReviewUpdateModalOpen = ref(false);

const route = useRoute();
const router = useRouter();
const comments = computed(() => communityStore.comments);
const reviewId = ref(route.params.reviewId);
const review = ref({});

const reviewLiked = ref(false);
const reviewHated = ref(false);
const reviewLikeCount = ref(0);
const reviewHateCount = ref(0);

const openReviewUpdateModal = () => {
  isReviewUpdateModalOpen.value = true;
};

const closeReviewUpdateModal = () => {
  isReviewUpdateModalOpen.value = false;
};

onMounted(() => {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1_1/${reviewId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      review.value = response.data;
    })
    .then(() => {
      communityStore.getComments(reviewId.value);
      console.log("코멘트", comments.value);
    });
});

onMounted(() => {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1_1/${reviewId.value}/like/${store.userId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      reviewLiked.value = response.data.liked;
      reviewLikeCount.value = response.data.count;
      console.log("리뷰 좋아요 조회 완료");
    })
    .catch((error) => {
      console.log(error);
    });
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1_1/${reviewId.value}/hate/${store.userId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      reviewHated.value = response.data.hated;
      reviewHateCount.value = response.data.count;
      console.log("리뷰 싫어요 조회 완료");
    })
    .catch((error) => {
      console.log(error);
    });
});

const reviewLike = function () {
  axios({
    method: "post",
    url: `http://127.0.0.1:8000/api/v1_1/${reviewId.value}/like/${store.userId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      reviewLiked.value = response.data.liked;
      reviewLikeCount.value = response.data.count;
      console.log("리뷰 좋아요 완료");
    })
    .catch((error) => {
      console.log(error);
    });
};

const reviewHate = function () {
  axios({
    method: "post",
    url: `http://127.0.0.1:8000/api/v1_1/${reviewId.value}/hate/${store.userId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      reviewHated.value = response.data.hated;
      reviewHateCount.value = response.data.count;
      console.log("리뷰 싫어요 완료");
    })
    .catch((error) => {
      console.log(error);
    });
};

const reviewDelete = function () {
  axios({
    method: "delete",
    url: `http://127.0.0.1:8000/api/v1_1/${reviewId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      console.log("리뷰 삭제 완료");
      router.push({ name: "community" });
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<style scoped>
.post-container {
  width: 500px;
  margin: 0 auto;
  background-color: #000000;
  border: 1px solid #dbdbdb;
  border-radius: 3px;
  padding: 20px;
  color: #fff; /* 글자 색상 추가 */
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
}

.post-image {
  width: 100%;
  margin-bottom: 10px;
}

.post-actions {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px;
}

.post-actions i {
  font-size: 24px;
  cursor: pointer;
}

.post-likes {
  font-weight: bold;
  margin-bottom: 10px;
}

.post-content {
  margin-bottom: 10px;
}

.post-comments {
  margin-bottom: 10px;
}

.add-comment {
  display: flex;
  justify-content: space-between;
}

.add-comment input {
  flex: 1;
  border: none;
  border-top: 1px solid #dbdbdb;
  padding: 10px;
}

.add-comment button {
  border: none;
  background: none;
  color: #3897f0;
  font-weight: bold;
  cursor: pointer;
  padding: 10px;
}

.like-button,
.hate-button {
  margin: 0;
}

.button-item {
  display: flex;
  align-items: center;
  font-size: 20px; /* 동일한 크기 설정 */
  color: white;
}

.modal-overlay-reviewcreate {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center; /* 중앙에 정렬 */
  z-index: 1100; /* 네비게이션 바 위에 위치 */
}

.modal-content-reviewcreate {
  background-color: #fff;
  padding: 10px;
  border-radius: 3px;
  width: 80%;
  max-width: 600px;
  max-height: 80%;
  overflow-y: auto;
  position: relative;
  color: #000; /* 글자 색상 추가 */
}

.close-reviewcreate {
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
</style>
