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
  course_par: number
  course_rating_9: number | null
  course_rating_18: number
  slope_rating: number
  holes: CourseHole[]
}

export interface CourseWithoutID {
  course_name: string
  course_par: number
  course_rating_9: number | null
  course_rating_18: number
  slope_rating: number
  holes: CourseHole[]
}

export interface FormData {
  round_number: number | undefined
  course: Course | undefined
  scores: number[]
}

export interface Round {
  round_number: number
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
