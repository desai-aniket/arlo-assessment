import requests


class UserDetails:

    url = ""
    headers = {""}
    #A Constructor to initialize the API details
    def __init__(self, url, headers):
        self.url = url
        self.headers=headers

    # A method that returns user details between the range of given ids
    def get_user_full_name_list(self, start_id, end_id):

        if not isinstance(start_id, int) or not isinstance(end_id, int):
            return []
        names = []

    # This is to set the total number of pages available in the service so to avoid hardcoding total no of pages
        response = requests.get(self.url, headers=self.headers, params={"page": 1})
        data = response.json()
        total_pages = data["total_pages"]

        for page in range(1, int(total_pages)):
            page_param = {"page": page}

            response = requests.get(self.url, headers=self.headers, params=page_param)

            if response.status_code == 200:
                data = response.json()
                users = data["data"]

                for user in users:
                    index = int(user["id"])
                    if (start_id <= index) and (index <= end_id):
                        full_name = user["first_name"] + " " + user["last_name"]
                        names.append(full_name)
            else:
                return []
        return sorted(names)



# A UserDetails object to initial total_pages
user = UserDetails("https://reqres.in/api/users", {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"})

assert user.get_user_full_name_list(1, 3) == ['Emma Wong', 'George Bluth', 'Janet Weaver']
assert user.get_user_full_name_list(5, 8) != ['Charles Morris', 'Emma Wong', 'Eve Holt', 'Janet Weaver']
assert user.get_user_full_name_list(1, "invalid_id") == []
assert user.get_user_full_name_list(-1, 3) == ['Emma Wong', 'George Bluth', 'Janet Weaver']
assert user.get_user_full_name_list(0, 0) == []

print("All assertions are passed!")
