<template>
  <div class="root">
      <button class="btn btn-success" @click="toggleModal">Загрузить работу</button>
      <div v-if="showModal" id="modalCreatePost" class="modalPost" @click.self="closeModal">
          <div class="modal-content">
              <span class="close" @click="closeModal">х</span>
              <form id="createForm" @submit.prevent="createPost">
                <br>
                  <textarea v-model="postTitle" placeholder="Введите заголовок работы" rows="3"
                          style="height: 100px; width: 910px; padding: 10px;"></textarea><br><br>
                          <input type="file"  class="form-control" id="postImages" @change="handleFileUpload" multiple >
                  <br>
                  <button type="submit" class="btn btn-success">Отправить</button>
              </form>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
      postTitle: '',
      postFile: null
    };
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
    },
    closeModal() {
      this.showModal = false;
    },
    handleFileUpload(event) {
      this.postFile = event.target.files[0];
    },
    async createPost() {
      const formData = new FormData();
      formData.append('content', this.postTitle);
      if (this.postFile) {
        console.log(this.postFile)
        formData.append('images', this.postFile);
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/wall/posts/create/', {
          method: 'POST',
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          },
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to create post');
        }

        const data = await response.json();
        console.log('Post created successfully:', data);
        this.closeModal();
        location.reload();
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
};
</script>

<style scoped>
.modalPost {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 50%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
}

.custom-file-input {
      display: none;
    }

    .custom-file-label {
      display: inline-block;
      background-color: #007bff;
      color: white;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 5px;
      transition: background-color 0.3s;
    }

    .custom-file-label:hover {
      background-color: #0056b3;
    }
</style>
