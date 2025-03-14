// Define the interface for a single hole
export interface CourseHole {
  hole: number
  par: number | undefined
  hdc: number | undefined
}

// Define the interface for a golf course
export interface Course {
  course_id: number
  course_name: string
  course_par_1_to_9: number | null
  course_par_10_to_18: number | null
  course_par_all: number | null
  course_rating_1_to_9: number | null
  course_rating_10_to_18: number | null
  course_rating_all: number | null
  slope_rating: number
  holes: CourseHole[]
}

export interface CourseWithoutID {
  course_name: string
  course_par_1_to_9: number | null
  course_par_10_to_18: number | null
  course_par_all: number | null
  course_rating_1_to_9: number | null
  course_rating_10_to_18: number | null
  course_rating_all: number | null
  slope_rating: number
  holes: CourseHole[]
}

export interface FormData {
  round_number: number | undefined
  date: string | undefined
  course: Course | undefined
  scores: number[]
}

export interface Round {
  round_number: number
  date: string
  user_id: number
  user: User
  calc_result_2020: number
  calc_result_2021: number
  course: Course
  scores: number[]
  score_differential: number
}

export interface CalculationResult {
  user_id: number | null
  calc_result: number[]
}

export interface User {
  first_name: string;
  last_name: string;
  user_id: number;
  email: string;
  role_id: number;
  created_at: string;
}

export interface LoginData {
  username : string;
  password: string;
}

export interface DecodedToken {
  role_id: number;
  expires: number;
  user_id: number;
}

export interface UserCreate{
  email: string
  password: string
  role_id: number
  first_name: string
  last_name: string
}

export interface ScorecardInput{
  HDC: number | undefined,
  course_id: number | undefined
}

export interface strokesAhead {
  course_HDC: number,
  hits_ahead: number[]
}


