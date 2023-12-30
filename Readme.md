# Auth 기능 구현 (주디 전화번호 회원가입 기반)

- 전화번호 회원가입
- 로그인
- 토큰 로그인

## 특징

- 범용적

## 특이사항

- 전화번호로만 회원가입 한다고 쳤을때는 username을 phone으로 둬야 할 수 있으나, email로 두는것이 가독성으로 향상으로 인해 유지보수 편의성이 향상된다 판단, 인증 방법의 확장성 면에서도 동일한 판단을 함.
  - (joody1@google.com, joody2@google.com || 010-0000-0000, 010-0000-0001)
- userAdmin readonly_fields 추가
  - ("last_login", "groups", "user_permissions")
