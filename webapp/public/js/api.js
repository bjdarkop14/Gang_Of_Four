(function main() {

    const baseUrl = "/api/";
    const userUrl = baseUrl + "user/";
    const areasUrl = baseUrl + "areas/";
    const groupUrl = baseUrl + "group/";
    const chatUrl = baseUrl + "chat/";

    function sendData(url, method, body) {
        return fetch(url, {
            method,
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body),
        })
    }

    async function handleErrors(response) {
        if (response.status === 204) {
            return {};
        };
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error);
        }
        return result;
    }

    function getTeams() {
        return fetch(teamUrl).then(Secret.execute).then(handleErrors);
    }

    function login(user) {
        return fetch(userUrl + "/login", "POST", user).then(handleErrors);
    }

    function postTeam(team) {
        return sendData(teamUrl, "POST", team).then(Secret.execute).then(handleErrors);
    }

    function putTeam(uuid, team) {
        return sendData(teamUrl + uuid, "PUT", team).then(Secret.execute).then(handleErrors);
    }

    function deleteTeam(uuid) {
        return fetch(teamUrl + uuid, {method: "DELETE"}).then(Secret.execute).then(handleErrors);
    }

    function getMember(id) {
        return fetch(memberUrl + id).then(Secret.execute).then(handleErrors);
    }

    function putMember(id, member) {
        return sendData(memberUrl + id, "PUT", member).then(Secret.execute).then(handleErrors);
    }

    function deleteMember(id) {
        return fetch(memberUrl + id, {method: "DELETE"}).then(Secret.execute).then(handleErrors);
    }
    
    window.API = {
        getTeams,
        postTeam,
        login,
        putTeam,
        deleteTeam,

        getMember,
        putMember,
        deleteMember,
    };
})();