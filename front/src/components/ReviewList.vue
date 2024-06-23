
<template>
  <div>
    <div class="card-container">
      <div v-for="review in store.reviews" :key="review.id" class="card" @click="goDetail(review.id)">
        <p>작성자 : {{ review.username }} </p>
        <p>리뷰 내용 : {{ truncateText(review.content, 100) }}</p>
        <p>평점 : {{ review.rank }}</p>
        <p>좋아요 : {{ review.like_users.length }}명 | 싫어요 :{{ review.hate_users.length }}명</p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { useCommunityStore } from '@/stores/community'
  import { useRouter } from "vue-router";

  const router = useRouter();
  const store = useCommunityStore()

  // 글자수 제한
  const truncateText = (text, limit) => {
  if (text.length <= limit) {
    return text;
  }
  return text.substring(0, limit) + '...';
  };

  // 리뷰 상세 정보 페이지 이동
  const goDetail = function (reviewId) {
  router.push({ name: "reviewDetail", params: { reviewId: reviewId } });
  };

</script>

<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.card {
  color: rgb(165, 165, 165);
  background-color: #1f1f1f;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 300px;
  height: 300px;
  margin: 10px;
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-10px);
  border: 1px solid #ff0000;
  color: white;
}

.card p {
  margin: 10px 0;
}
</style>



<!-- <p>
  작성자 : {{ review.username }} | 리뷰 내용 : {{ review.content }} | 리뷰 평점 : {{ review.rank }} | 좋아요 : 
  <span v-if="review.like_users.length">{{ review.like_users.length }}</span>
  <span v-else>0</span>명 | 싫어요 : 
  <span v-if="review.hate_users.length">{{ review.hate_users.length }}</span>
  <span v-else>0</span>명
</p> -->