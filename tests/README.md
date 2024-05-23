## Pytest Details

### Why I prefer test functions

1. To check that you are right
2. New features do not affect old endpoints

### Make sure the pytest-asyncio is in  v0.21.2


<b> 12/5/2025 🧪</b> 


<a href="./conftest.py"> conftest.py </a> contains 
    
Creating engine and session_maker for the test DB
Creating a override dependency to return the session for above session_maker
dependency_overroide for the get_session for the test_db
Make a event Loop
Creating new table and inserting demo datas for the test purpose
Making a async_client fixture for the client export.

<ol>
    <li>Creating engine and session_maker for the test DB</li>
    <li>Creating a override dependency to return the session for above session_maker</li>
    <li>dependency_overroide for the get_session for the test_db</li>
    <li>Make a event Loop</li>
    <li>Creating new table and inserting demo datas for the test purpose</li>
    <li>Making a async_client fixture for the client export.</li>
</ol>

<br/>

<a href="./tester/test_endpoints.py">tester/test_endpoints.py</a> contains

<ol>
    <li>health check <b style="padding-left:30px;"> "/health"</b></li>
    <li>Create User <b style="padding-left:30px;"> "/register"</b></li>
    <li>Basic login <b style="padding-left:30px;"> "/login"</b></li>
    <li>Getting token status <b style="padding-left:30px;"> "/token"</b></li>
    <li>Get profile detils of the same (new_user_data_1) user  <b style="padding-left:30px;"> "/profile/{user_id}"</b></li>  
    <li>Get profile detils of the other (new_user_data_2) user user <b style="padding-left:30px;"> "/profile/{user_id}"</b></li>
    <li>Update the user (new_user_data_1) uri's <b style="padding-left:30px;"> "/update_user"</b></li>
    <li>Get updated uri of user (new_user_data_1) <b style="padding-left:30px;"> "/update_uri"</b></li>
    <li>Test logout<b style="padding-left:30px;"> "/logout"</b></li>
</ol>

all test 😁 results passed
<img src="./../Assets/test_results/2024-05-13 004306.png" alt="test_on_2025-05-13"/>


