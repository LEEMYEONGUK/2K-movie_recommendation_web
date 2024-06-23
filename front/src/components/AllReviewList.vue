<template>
  <div>
    <div id="box">
      <img
        class="img me-3"
        :src="`https://image.tmdb.org/t/p/w500${review.poster_path}`"
        alt="..."
      />
      <div class="overlay text-white">

        <p class="fs-5">{{ truncateText(review.title, 50) }}</p>
        <p class="fs-5"><i class="bi bi-star-fill star"></i> {{ review.rank }} </p>
        <RouterLink
          :to="{ name: 'reviewDetail', params: { reviewId: review.id } }"
          class="main-text btn btn-outline-danger mb-5"
          >
          리뷰 상세보기
        </RouterLink
        >
      </div>
    </div>
  </div>


  
</template>

<script setup>
const props = defineProps({
  review: Object,
});

const truncateText = (text, limit) => {
  if (text.length <= limit) {
    return text;
  }
  return text.substring(0, limit) + '...';
};
</script>

<style scoped>
.img {
  width: 200px;
}


#box {
  width: 100%; /* 부모 컨테이너의 너비를 가득 채움 */
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin: 0; /* 여백을 제거하여 부모 컨테이너에 맞춤 */
  transition: all 0.3s cubic-bezier(0.42, 0.0, 0.58, 1.0);
  position: relative; /* overlay 위치 설정을 위해 추가 */
}

#box:hover {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
  transform: translateY(-10px);
}

#box .img {
  display: block;
  width: 100%; /* 이미지가 박스의 너비에 맞춰지도록 */
  height: 100%;
}

#box .heading {
  font-size: 18px;
  color: white;
  font-weight: bolder;
}

#box .texts {
  font-size: 14px;
  line-height: 18px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}

#box:hover .overlay {
  opacity: 1;
  pointer-events: auto;
}

.star {
  color: yellow;
}
</style>
