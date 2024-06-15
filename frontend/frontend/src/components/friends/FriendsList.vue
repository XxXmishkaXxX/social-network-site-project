<template>
    <div>
        <ul class="list-group" v-if="friends.length > 0">
            <li v-for="friend in friends" :key="friend.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <img :src="friend.user_profile.avatar" alt="avatar" class="rounded-circle me-3" width="50" height="50">
                    <div>
                        <h5 class="mb-0">
                            <a :href="`/wall/${friend.friend}/`" class="friend-name">{{ friend.user_profile.full_name }}</a>
                        </h5>
                        <small>{{ friend.university }}</small>
                    </div>
                </div>
                <div>
                    <a href="#" class="btn btn-link">Написать сообщение</a>
                </div>
            </li>
        </ul>
        <p v-else-if="friends && friends.length === 0" class="text-center">У вас нет добавленных друзей.</p>
    </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '../../config';

export default{
    data() {
        return {
            friends: []
        }
    },
    mounted() {
        this.getFriends();
    },

    methods: {
        async getFriends() {
            try {
                const response = await axios.get(`${API_BASE_URL}/relations/friends/`, {
                    headers: {
                        'Authorization': `token ${localStorage.getItem('token')}`
                    }
                });
                this.friends = response.data;
                console.log(this.friends)
            } catch (error) {
                console.error('Error fetching friends:', error);
            }
        }
    }

}
</script>

<style scoped>

.friend-name {
    color: inherit;
    text-decoration:none;
}
.list-group-item {
    border: none;
    padding: 15px 20px;
    margin-bottom: 10px;
    background-color: #f8f9fa;
    border-radius: 8px;
}
</style>