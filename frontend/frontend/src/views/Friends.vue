<template>
    <div class="d-flex flex-column min-vh-100">
        <Navbar />
        <div class="main-container d-flex flex-row flex-grow-1">
            <SideBar />
            <div class="container-friends flex-grow-1">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <button class="btn btn-outline-primary" @click="showFriendsList">Все друзья</button>
                    </div>
                    <div class="ml-auto">
                        <button class="btn btn-outline-primary me-2" @click="showSearchPeopleForm">Поиск людей</button>
                        <button class="btn btn-outline-primary me-2" @click="showIncomingUsersList">Входящие</button>
                        <button class="btn btn-outline-primary" @click="showOutgoingUsersList">Исходящие</button>
                    </div>
                </div>
                <FriendsList v-if="currentComponent === 'FriendsList'" />
                <IncomingUsersList v-if="currentComponent === 'IncomingUsersList'" />
                <OutgoingUsersList v-if="currentComponent === 'OutgoingUsersList'" />
                <SearchPeople v-if="currentComponent === 'SearchPeople'" />
            </div>
        </div>
        <Footer />
    </div>
</template>
<script>

import Navbar from '../components/base/Navbar.vue'
import Footer from '../components/base/Footer.vue'
import FriendsList from '../components/friends/FriendsList.vue'
import OutgoingUsersList from '../components/friends/OutgoingUsersList.vue'
import IncomingUsersList from '../components/friends/IncomingUsersList.vue'
import SearchPeople from '../components/friends/SearchPeople.vue'
import SideBar from '@/components/base/SideBar.vue'

export default {
    components: { 
        Navbar,
        Footer,
        FriendsList,
        OutgoingUsersList,
        IncomingUsersList,
        SearchPeople,
        SideBar
    },
    data() {
        return {
            currentComponent: 'FriendsList',
        }
    },
    methods:{
        showFriendsList() {
                this.currentComponent = 'FriendsList';
            },
        showIncomingUsersList() {
                this.currentComponent = 'IncomingUsersList';
            },
        showOutgoingUsersList() {
                this.currentComponent = 'OutgoingUsersList';
            },
        showSearchPeopleForm() {
            this.currentComponent = 'SearchPeople';
        }
        }
}
</script>





<style scoped>
.main-container {
    margin: 10px 10px 200px 200px;
    width: 80%;
    flex-direction: column;
    align-items: flex-start;
}
.container-friends {
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 800px;
    padding-bottom: 20px;
    margin-left: 20px;
    min-height: 500px; /* Задаем минимальную высоту контейнера */
    max-height: 100%
}

.list-group-item {
    border: none;
    padding: 15px 20px;
    margin-bottom: 10px;
    background-color: #f8f9fa;
    border-radius: 8px;
}

.btn-link {
    color: #007bff;
}

.btn-link:hover {
    color: #0056b3;
    text-decoration: underline;
}

.badge {
    font-size: 90%;
}


.dropdown-toggle::after {
    margin-left: 0.255em;
}
.friend-name {
    color: inherit;
    text-decoration:none;
}

.main-container {
    display: flex;
    flex-direction: row;
    flex-grow: 1;
}


footer {
    margin-top: auto; /* Закрепить футер внизу страницы */
}
</style>