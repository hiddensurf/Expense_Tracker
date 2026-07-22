from fastapi import HTTPException, status
credential_exception_security=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Could not validate credentials",
                                            headers={"WWW-Authenticate":"Bearer"})
credential_exception_routes=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Invalid username or password",
                                            headers={"WWW-Authenticate":"Bearer"})
disabled_user_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                      detail="Account is inactive")