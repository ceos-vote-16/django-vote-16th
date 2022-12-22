### 배포 

http://3.38.123.37/api/
*****

### ERD 구성
<img width="800" alt="스크린샷 2022-12-22 오후 8 40 37" src="https://user-images.githubusercontent.com/62806067/209127037-06e00c10-aa87-424a-a8a5-1057250e768c.png">

### API명세서
#### [Teample API 명세서](https://www.notion.so/shjeong1026/CEOS-VOTE-API-4c84ab53d37a47f39855092265495f3f)
*****

### 회원가입/로그인
1. dj-rest-auth 사용
2. Register필드 추가를 위해 RegisterSerializer 커스텀 및 DefaultAccountAdapter 커스텀
3. userDetail 페이지 필드 추가 및 삭제를 위해 auth_serializers.UserDetail 커스텀
4. Register 추가 필드 특정 값 외 회원가입 방지를 위해 user_register_input_validation 생성 및    
   RegisterSerializer의 validate 커스텀
5. BaseUserManager커스텀으로 usernamer 필수 필드로 설정

### 투표
1. Get요청 시 auth 정보 필요 없어도 되도록 IsAuthenticatedInPutReq 생성 /BasePermission 커스텀
2. put요청 시 특정 팀 및 후보자 투표만 가능하도록 update(viewset의 put)커스텀 및 validator 생성, 적용
3. put요청 시 body로 부터 정보 받아오기 위해 lookup_value로 받아줌
4. response 간결하게 하기 위해 custom_response 생성

### 문제 사항
auth부분에서 logout만 실행이 안된적이 있는데 auth가 장고 버전과 맞지 않아 생긴 문제    
로컬에선 제대로 돌아갔으나 배포 시 충돌되어 서버에러 발생으로 예상   
깃헙 액션 에러문구를 잘 봐야할 것 같다.
