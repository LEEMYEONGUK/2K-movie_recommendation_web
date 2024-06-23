import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

export const useCommunityStore = defineStore("community",() => {
    const reviews = ref([])
    const comments = ref([])
    const store = useUserStore()
    const router = useRouter()
    
    const reviewLiked = ref(false)
    const reviewHated = ref(false)
    const reviewLikeCount = ref(0)
    const reviewHateCount = ref(0)

    // 리뷰 조회
    const getReviews = function () {
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/api/v1_1/reviews/",
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        console.log("리뷰 조회 완료")
        reviews.value = response.data
      });
    };

    // 리뷰 작성
    const createReview = function (data) {
      const { title, movie_title, content, rank, user, poster_path, username } = data
      axios({
        method: "post",
        url: "http://127.0.0.1:8000/api/v1_1/reviews/",
        data: {
          title,
          movie_title,
          rank,
          content,
          user,
          poster_path,
          username
        },
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        console.log("리뷰 작성 완료")
        getReviews()
      })
        .catch((error) => {
          console.log(error)
        })
    };

    const updateReview = function (data) {
      const { title, movie_title, content, rank, user, poster_path, username, reviewId } = data
      axios({
        method: "put",
        url: `http://127.0.0.1:8000/api/v1_1/${reviewId}/`,
        data: {
          title,
          movie_title,
          rank,
          content,
          user,
          poster_path,
          username
        },
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        console.log("리뷰 수정 완료")
        // router.push({name:'reviewDetail', params:{reviewId:reviewId}})
        router.push({name:'community'})
      })
        .catch((error) => {
          console.log(error)
        })
    };

    // 리뷰<-댓글 조회
    const getComments = function (review) {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/v1_1/${review}/comment/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        console.log("댓글 조회 완료")
        comments.value = response.data
      });
    };

    // 리뷰<-댓글 생성
    const createComment = function (data) {
      const { content, user, review } = data
      axios({
        method: "post",
        url:`http://127.0.0.1:8000/api/v1_1/${review}/comment/`,
        data: {
          content, user, review
        },
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        console.log("댓글 작성 완료")
        getComments(review)

      })
        .catch((error) => {
          console.log(error)
        })
    }

    // 리뷰 좋아요
    const reviewLike = function (data) {
      const { user, review } = data
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/v1_1/${review}/like/${user}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        reviewLiked.value = response.data.liked
        reviewLikeCount.value = response.data.count
        console.log("리뷰 좋아요 완료")
      })
        .catch((error) => {
          console.log(error)
      })
    }

    // 리뷰 싫어요
    const reviewHate = function (data) {
      const { user, review } = data
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/v1_1/${review}/hate/${user}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response)
        reviewHated.value = response.data.hated
        reviewHateCount.value = response.data.count
        console.log("리뷰 싫어요 완료")
      })
        .catch((error) => {
          console.log(error)
      })
    }

    const getMovieReview = function (movieTitle) {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/v1_1/reviews/${movieTitle}`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      }).then((response) => {
        console.log(response);
        console.log("영화 댓글 조회 완료")
        reviews.value = response.data
        reviews.value.sort((a, b) => b.like_users.length - a.like_users.length)
      })
    }

    return { 
      reviews,
      comments,
      getReviews,
      createReview,
      updateReview,
      getComments,
      createComment,
      reviewLiked,
      reviewHated,
      reviewLikeCount,
      reviewHateCount,
      reviewLike,
      reviewHate,
      getMovieReview };
  },
  { persist: true }
)
